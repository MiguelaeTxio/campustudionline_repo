# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/tasks.py
import logging
import traceback
import os
import json
import time
import re
from datetime import datetime, timedelta
import pytz

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django import db
from django.db import transaction
from django.db.models import Count, Q, F
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from google.api_core.exceptions import ResourceExhausted, DeadlineExceeded

from .models import AutomationSettings, ApiKey, PendingContentTask, GeneratedContentChunk, ContentRequest
from academic_structure.models import Subject
from users.models import CustomUser
from assessment.models import Assessment, Question, UserAnswer, AssessmentSettings
from contents.models import (
    ContentMaterial,
    FreeContentMasterCategory,
    FreeContentSubCategory,
)
from core.services.gemini_service import generate_text_content, clean_json_response, AIServiceCriticalError
from core.services.gemini_schemas import ASSESSMENT_CORRECTION_SCHEMA
from core.services.prompt_generators import (
    generate_course_metadata_prompt,
    generate_master_schema_prompt,
    generate_atomic_content_prompt,
)
from messaging.push_utils import send_notification_to_user
from core.utils import send_unified_notification


logger = logging.getLogger(__name__)
User = get_user_model()

QUARANTINE_MAILBOX_FILE = "/home/MiguelAeTxio/SWAP/quarantine_requests.log"

# ==============================================================================
# SECCIÓN 1: FUNCIONES AUXILIARES DEL ORQUESTADOR
# ==============================================================================

def _log_structured_event(message: str, level: str = "INFO", details: dict = None):
    try:
        settings = AutomationSettings.load()
        log_entry = {
            "timestamp": timezone.now().isoformat(),
            "level": level,
            "message": message,
            "details": details or {}
        }
        settings.event_log.insert(0, log_entry)
        settings.event_log = settings.event_log[:100]
        settings.save(update_fields=['event_log'])
    except Exception as e:
        logger.error(f"CRITICAL: No se pudo escribir en el event_log estructurado: {e}", exc_info=True)

def _send_admin_notification(title, body):
    try:
        admins = CustomUser.objects.filter(is_superuser=True, is_active=True)
        if not admins.exists():
            logger.warning("No se encontraron administradores activos para notificar.")
            return
        email_subject = f"[CampuStudiOnline Automation] {title}"
        recipient_list = [admin.email for admin in admins]
        context = {
            'title': title,
            'message_body': body,
            'dashboard_url': 'https://www.campustudionline.com/admin/orchestrator/automationsettings/1/change/'
        }
        html_message = render_to_string('orchestrator/email/admin_notification.html', context)
        
        send_mail(
            subject=email_subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=True,
            html_message=html_message
        )
        logger.info(f"Notificación de administrador enviada a {len(recipient_list)} admin(s): '{title}'")
    except Exception as e:
        logger.error(f"Error al enviar notificación de administrador: {e}", exc_info=True)

def _process_quarantine_requests():
    if not os.path.exists(QUARANTINE_MAILBOX_FILE):
        return
    try:
        with open(QUARANTINE_MAILBOX_FILE, "r") as f:
            key_ids_to_quarantine = set(line.strip() for line in f if line.strip().isdigit())
        if not key_ids_to_quarantine:
            os.remove(QUARANTINE_MAILBOX_FILE)
            return
        _log_structured_event(f"PROCESANDO BUZÓN: Se encontraron {len(key_ids_to_quarantine)} solicitudes de cuarentena.", "INFO", {"key_ids": list(key_ids_to_quarantine)})
        with transaction.atomic():
            keys_to_update = ApiKey.objects.select_for_update().filter(id__in=key_ids_to_quarantine, is_quarantined=False)
            if not keys_to_update.exists():
                os.remove(QUARANTINE_MAILBOX_FILE)
                return
            key_names = list(keys_to_update.values_list('name', flat=True))
            updated_count = keys_to_update.update(is_quarantined=True)
        if updated_count > 0:
            message = f"BUZÓN PROCESADO: {updated_count} clave(s) han sido puestas en cuarentena: {', '.join(key_names)}."
            _log_structured_event(message, "WARNING")
            _send_admin_notification("Clave(s) API en Cuarentena (vía Buzón)", message)
        os.remove(QUARANTINE_MAILBOX_FILE)
    except Exception as e:
        logger.critical(f"FALLO CRÍTICO EN PROCESADOR DE BUZÓN: No se pudo procesar '{QUARANTINE_MAILBOX_FILE}': {e}", exc_info=True)

def _check_and_perform_daily_reset():
    try:
        automation_settings = AutomationSettings.load()
        madrid_tz = pytz.timezone('Europe/Madrid')
        now_madrid = timezone.now().astimezone(madrid_tz)
        today = now_madrid.date()
        if automation_settings.last_quarantine_reset_date >= today:
            return
        now_time = now_madrid.time()
        if now_time >= automation_settings.quarantine_reset_time:
            keys_to_reset = ApiKey.objects.filter(is_quarantined=True)
            count = keys_to_reset.count()
            if count > 0:
                keys_to_reset.update(is_quarantined=False)
                message = f"Se han liberado {count} claves API de la cuarentena."
                _log_structured_event(f"RESET DIARIO (INTEGRADO): {message}", "INFO")
                _send_admin_notification("Reseteo Diario de Claves API", message)
            automation_settings.last_quarantine_reset_date = today
            automation_settings.save(update_fields=["last_quarantine_reset_date"])
    except Exception as e:
        _log_structured_event(f"Error CRÍTICO en la lógica de reseteo diario integrado: {e}", "CRITICAL", {"traceback": traceback.format_exc()})
        logger.critical(f"Error CRÍTICO en _check_and_perform_daily_reset: {e}", exc_info=True)


def _purge_zombie_tasks():
    try:
        # [FIX] Umbral aumentado a 24 horas para evitar borrar tareas en cola larga
        threshold = timezone.now() - timedelta(hours=24)
        
        # Identificar tareas realmente abandonadas (sin tocar PENDING ni estados de espera)
        zombies = PendingContentTask.objects.exclude(
            status__in=[
                PendingContentTask.StatusChoices.PROCESSING, 
                PendingContentTask.StatusChoices.COMPLETED, 
                PendingContentTask.StatusChoices.FAILED_FATAL,
                PendingContentTask.StatusChoices.PENDING,
                PendingContentTask.StatusChoices.FAILED_RETRYABLE,
                PendingContentTask.StatusChoices.FAILED_QUOTA
            ]
        ).filter(updated_at__lt=threshold)
        
        count = zombies.count()
        if count > 0:
            # Borrado masivo
            zombies.delete()
            _log_structured_event(f"LIMPIEZA AUTOMÁTICA: Se han eliminado {count} tareas residuales inactivas por >24h.", "WARNING")
    except Exception as e:
        logger.error(f"Error en limpieza de zombies: {e}")

def _get_next_subject_queryset(settings):
    base_queryset = Subject.objects.filter(content_materials__isnull=True)
    active_task_subject_names = PendingContentTask.objects.exclude(
        status__in=[PendingContentTask.StatusChoices.COMPLETED, PendingContentTask.StatusChoices.FAILED_FATAL]
    ).values_list('subject__name', flat=True).distinct()
    query = base_queryset.exclude(name__in=active_task_subject_names)
    if settings.seed_branch:
        query = query.filter(academic_year__degree__branch=settings.seed_branch)
    if settings.seed_degree:
        query = query.filter(academic_year__degree=settings.seed_degree)
    if settings.seed_year:
        try:
            year_map = {"Primero": 1, "Segundo": 2, "Tercero": 3, "Cuarto": 4, "Quinto": 5}
            year_int = year_map.get(settings.seed_year)
            if year_int:
                query = query.filter(academic_year__year=year_int)
        except (ValueError, TypeError):
            pass
    return query

def _advance_seed_filters_if_needed(automation_settings):
    if not any([automation_settings.seed_branch, automation_settings.seed_degree, automation_settings.seed_year]):
        return False
    if not _get_next_subject_queryset(automation_settings).exists():
        notification_title = "Lote de Generación Completado"
        message = ""
        if automation_settings.seed_year:
            message = f"Lote para '{automation_settings.seed_year}' del grado '{automation_settings.seed_degree.name}' completado. Se elimina filtro de año y se continúa."
            automation_settings.seed_year = ""
            automation_settings.save(update_fields=['seed_year'])
            _log_structured_event(message)
            _send_admin_notification(notification_title, message)
            return True
        if automation_settings.seed_degree:
            message = f"Lote para el grado '{automation_settings.seed_degree.name}' completado. Se elimina filtro de grado y se continúa."
            automation_settings.seed_degree = None
            automation_settings.save(update_fields=['seed_degree'])
            _log_structured_event(message)
            _send_admin_notification(notification_title, message)
            return True
        if automation_settings.seed_branch:
            message = f"Lote para la rama '{automation_settings.seed_branch.name}' completado. Se elimina filtro de rama y se continúa."
            automation_settings.seed_branch = None
            automation_settings.save(update_fields=['seed_branch'])
            _log_structured_event(message)
            _send_admin_notification(notification_title, message)
            return True
    return False

# ==============================================================================
# SECCIÓN 2: FUNCIONES AUXILIARES DE GENERACIÓN DE CONTENIDO
# ==============================================================================

def _request_quarantine_via_mailbox(api_key: ApiKey):
    try:
        with open(QUARANTINE_MAILBOX_FILE, "a") as f:
            f.write(f"{api_key.id}\n")
        logger.warning(f"BUZÓN: Solicitud de cuarentena enviada para la clave '{api_key.name}' (ID: {api_key.id}).")
    except Exception as e:
        logger.critical(f"FALLO CRÍTICO DE ARQUITECTURA: No se pudo escribir en el buzón de cuarentena '{QUARANTINE_MAILBOX_FILE}': {e}", exc_info=True)

def log_assessment_task_event(assessment_id, message, level="INFO", payload=None):
    """
    [PAIR] Implementación espejo de log_task_event para Assessments.
    Garantiza persistencia atómica de logs independientemente del flujo principal.
    """
    try:
        from assessment.models import Assessment
        timestamp = datetime.utcnow().isoformat() + "Z"
        entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
        }
        if payload:
            try:
                # [SAFETY] Truncate massive payloads to prevent database bloat
                payload_str = json.dumps(payload, ensure_ascii=False, sort_keys=True)
                if len(payload_str) > 2000:
                    entry["payload"] = payload_str[:2000] + " ... [TRUNCATED]"
                else:
                    entry["payload"] = payload_str
            except TypeError:
                entry["payload"] = str(payload)[:2000]

        with transaction.atomic():
            assessment = Assessment.objects.select_for_update().get(pk=assessment_id)
            if assessment.event_log is None:
                assessment.event_log = []
            if isinstance(assessment.event_log, list):
                assessment.event_log.insert(0, entry)
                assessment.event_log = assessment.event_log[:100]
            assessment.save(update_fields=['event_log'])
    except Exception as e:
        logger.error(f"Error al escribir en event_log DB para Assessment {assessment_id}: {e}")

def log_task_event(task_id: str, message: str, is_error: bool = False, payload: dict = None):
    try:
        timestamp = datetime.utcnow().isoformat() + "Z"
        entry = {
            "timestamp": timestamp,
            "level": "ERROR" if is_error else "INFO",
            "message": message,
        }
        if payload:
            try:
                # [SAFETY] Truncate massive payloads to prevent database bloat
                payload_str = json.dumps(payload, ensure_ascii=False, sort_keys=True)
                if len(payload_str) > 2000:
                    entry["payload"] = payload_str[:2000] + " ... [TRUNCATED]"
                else:
                    entry["payload"] = payload_str
            except TypeError:
                entry["payload"] = str(payload)[:2000]
        with transaction.atomic():
            task = PendingContentTask.objects.select_for_update().get(id=task_id)
            if task.task_log is None:
                task.task_log = []
            if isinstance(task.task_log, list):
                task.task_log.append(entry)
            task.save(update_fields=['task_log'])
    except Exception as e:
        logger.error(f"Error al escribir en task_log DB para {task_id}: {e}")

def _parse_master_schema(markdown_text: str) -> list:
    headings = re.findall(r"^(##+)\s(.*)", markdown_text, re.MULTILINE)
    return [(len(hashes), title.strip()) for hashes, title in headings]

def _parse_markdown_with_separator(raw_text: str) -> tuple[str, str]:
    # Regex flexible para encontrar el separador (case insensitive, con/sin espacios, guiones o hashtags)
    # Ejemplos: "---FUENTES---", "## Fuentes", "--- Bibliografía ---"
    separator_pattern = r"(?i:^[-*_#]*\s*(?:FUENTES|BIBLIOGRAF[ÍI]A|REFERENCIAS)\s*[-*_#]*$)"
    
    # Buscar todas las coincidencias
    matches = list(re.finditer(separator_pattern, raw_text, re.MULTILINE))
    
    if matches:
        # Usar la última coincidencia válida para dividir
        last_match = matches[-1]
        content = raw_text[:last_match.start()].strip()
        sources = raw_text[last_match.end():].strip()
        return content, sources
    else:
        logger.warning("El separador '---FUENTES---' (o variante) no se encontró. Tratando todo como contenido.")
        return raw_text.strip(), ""

def _assemble_final_markdown_from_chunks(course_title: str, metadata: dict, master_schema: str, chunks: list[GeneratedContentChunk]) -> str:
    classification = metadata.get("clasificacion_intelectual", {})
    yaml_header = ["---", f'titulo: "{course_title}"', f"descripcion_corta: \"{metadata.get('descripcion_corta', '')}\"", f"categoria_general: \"{classification.get('categoria_general', 'Desconocida')}\"", f"subcategoria: \"{classification.get('subcategoria', 'Desconocida')}\"", f"palabras_clave: {json.dumps(classification.get('palabras_clave', []))}", "---"]
    parsed_schema = _parse_master_schema(master_schema)
    fuentes_title = "Fuentes y Bibliografía"
    fuentes_slug = slugify(fuentes_title)
    parsed_schema.append((2, fuentes_title))
    toc_entries = []
    for level, title in parsed_schema:
        slug = slugify(title)
        indent = "    " * (level - 2)
        toc_entries.append(f"{indent}*   [{title}](#{slug})")
    introduction = [f"# {course_title}", f"{metadata.get('descripcion_corta', 'Descripción no disponible.')}", '<a id="tabla-de-contenidos"></a>', "## Tabla de Contenidos", "\n".join(toc_entries)]
    content_body = []
    original_parsed_schema = _parse_master_schema(master_schema)
    chunk_map = {slugify(original_parsed_schema[chunk.order - 1][1]): chunk for chunk in chunks}
    for level, title in original_parsed_schema:
        slug = slugify(title)
        chunk = chunk_map.get(slug)
        content = chunk.content if chunk else f"### Error\n\nEl contenido para la sección '{title}' no pudo ser localizado."
        heading_hashes = "#" * level
        content_body.append(f'<a id="{slug}"></a>')
        content_body.append(f"{heading_hashes} {title}")
        content_body.append(content)
        if level == 2:
            content_body.append("\n[⬆️ Volver al índice](#tabla-de-contenidos)")
    all_sources_text = [chunk.ai_sources for chunk in chunks if chunk.ai_sources]
    if all_sources_text:
        unique_references = set()
        for source_block in all_sources_text:
            for line in source_block.split('\n'):
                cleaned_line = line.strip()
                if cleaned_line:
                    unique_references.add(cleaned_line)
        sorted_references = sorted(list(unique_references))
        formatted_bibliography = "\n".join(f"- {ref}" for ref in sorted_references)
        bibliography_section = [f'<a id="{fuentes_slug}"></a>', f"## {fuentes_title}", formatted_bibliography, "\n[⬆️ Volver al índice](#tabla-de-contenidos)"]
        content_body.extend(bibliography_section)
    final_parts = yaml_header + introduction + content_body
    return "\n\n".join(final_parts)

def _get_or_create_free_categories_from_classification(classification_data: dict, course_title: str) -> tuple:
    master_name = classification_data.get("categoria_general")
    sub_name = classification_data.get("subcategoria")
    if not master_name:
        logger.warning(f"No se encontró 'categoria_general' en la clasificación para '{course_title}'. No se puede clasificar.")
        return None, None
    master_category, _ = FreeContentMasterCategory.objects.get_or_create(name=master_name)
    sub_category = None
    if sub_name:
        sub_category, _ = FreeContentSubCategory.objects.get_or_create(master_category=master_category, name=sub_name)
    return master_category, sub_category

def _send_completion_notifications(new_content: ContentMaterial):
    try:
        first_subject = new_content.subject.first()
        if not first_subject: return
        content_request = ContentRequest.objects.filter(subject=first_subject).first()
        if not content_request: return
        requesters = content_request.requesters.all()
        if not requesters: return
        logger.info(f"Enviando notificaciones de finalización para '{new_content.title}' a {requesters.count()} usuarios.")
        content_url = new_content.get_absolute_url()
        full_url = f"https://{settings.ALLOWED_HOSTS[0]}{content_url}"
        push_title = "¡Contenido Disponible!"
        push_body = f"El material de estudio para '{new_content.title}' que solicitaste ya está disponible."
        email_subject = f"[CampuStudiOnline] El contenido para '{new_content.title}' está listo"
        email_body_text = (f"¡Hola!\n\nNos complace informarte que el material de estudio para la asignatura '{new_content.title}' que solicitaste ha sido generado y ya está disponible en la plataforma.\n\n"
                           f"Puedes acceder a él directamente a través del siguiente enlace:\n{full_url}\n\n"
                           f"Gracias por tu paciencia y por ayudarnos a mejorar CampuStudiOnline.\n\n"
                           f"Atentamente,\nEl equipo de CampuStudiOnline")
        context = {
            'content_title': new_content.title,
            'content_url': full_url
        }
        html_message = render_to_string('orchestrator/email/content_completion.html', context)

        for user in requesters:
            send_notification_to_user(user, push_title, push_body, url=content_url)
            send_mail(
                subject=email_subject, 
                message=email_body_text, 
                from_email=settings.DEFAULT_FROM_EMAIL, 
                recipient_list=[user.email], 
                fail_silently=False,
                html_message=html_message
            )
        content_request.status = ContentRequest.StatusChoices.FULFILLED
        content_request.save(update_fields=["status"])
        logger.info(f"La solicitud de contenido para '{first_subject.name}' ha sido marcada como 'Satisfecha'.")
    except Exception as e:
        logger.error(f"Error al enviar notificaciones de finalización para el contenido {new_content.id}: {e}", exc_info=True)

# ==============================================================================
# SECCIÓN 3: FUNCIONES AUXILIARES DE AUTOEVALUACIONES (ASSESSMENT)
# ==============================================================================

def log_timestamp(message):
    logger.info(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] {message}")
    try:
        from assessment.models import AssessmentSettings
        s = AssessmentSettings.get_settings()
        entry = {"timestamp": timezone.now().isoformat(), "message": str(message)}
        if s.event_log is None: s.event_log = []
        s.event_log.insert(0, entry)
        s.event_log = s.event_log[:100]
        s.save(update_fields=["event_log"])
    except Exception:
        pass

def _log_assessment_event(assessment_id, message, level="INFO"):
    """Wrapper para usar el método atómico del modelo."""
    try:
        with transaction.atomic():
            assessment = Assessment.objects.select_for_update().get(pk=assessment_id)
            assessment.add_log_event(message, level)
    except Assessment.DoesNotExist:
        logger.error(f"No se pudo loguear evento para Assessment {assessment_id}: No existe.")
    except Exception as e:
        logger.error(f"Error escribiendo log de Assessment {assessment_id}: {e}")

def _parse_assessment_text(text: str) -> list:
    questions = []
    pattern = re.compile(
        r"\[---PREGUNTA---\](.*?)" r"\[---RESPUESTA---\](.*?)" r"\[---FIN-PREGUNTA---\]",
        re.DOTALL,
    )
    matches = pattern.findall(text)
    for match in matches:
        question_text = match[0].strip()
        model_answer = match[1].strip()
        if question_text and model_answer:
            questions.append({"question_text": question_text, "model_answer": model_answer})
    return questions

def _parse_correction_text(text: str) -> dict:
    score = None
    feedback = ""
    score_match = re.search(r"PUNTUACION:\s*(\d+)", text, re.IGNORECASE)
    if score_match:
        try:
            score = int(score_match.group(1))
            if not (0 <= score <= 100): score = None
        except (ValueError, IndexError):
            score = None
    feedback_match = re.search(r"FEEDBACK:\s*(.*)", text, re.DOTALL | re.IGNORECASE)
    if feedback_match:
        feedback = feedback_match.group(1).strip()
    return {"score": score, "feedback": feedback}

# ==============================================================================
# SECCIÓN 4: TAREAS CELERY
# ==============================================================================

class ContentGenerationError(Exception):
    pass

@shared_task(bind=True)
def global_orchestrator_task(self):
    try:
        _purge_zombie_tasks()  # [NUEVO] Limpieza preventiva de zombies
        _process_quarantine_requests()
        _check_and_perform_daily_reset()
        db.close_old_connections()
        automation_settings = AutomationSettings.load()
        if not automation_settings.is_running:
            status_msg = "DETENIDO: Interruptor maestro desactivado."
            if automation_settings.last_run_status != status_msg:
                _log_structured_event(status_msg, "INFO")
                automation_settings.last_run_status = status_msg
                automation_settings.save(update_fields=['last_run_status'])
            return
        active_key = automation_settings.active_api_key
        if not active_key or not active_key.is_enabled or active_key.is_quarantined:
            _log_structured_event(f"SINCRO: Clave activa ('{active_key.name if active_key else 'N/A'}') no es válida. Buscando reemplazo.", "INFO")
            next_available_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
            if next_available_key:
                automation_settings.active_api_key = next_available_key
                automation_settings.save(update_fields=['active_api_key'])
                _log_structured_event(f"SINCRO EXITOSA: Nueva clave activa es '{next_available_key.name}'.", "INFO", {"new_api_key_id": next_available_key.id})
            else:
                madrid_tz = pytz.timezone('Europe/Madrid')
                now_madrid = timezone.now().astimezone(madrid_tz)
                reset_time = automation_settings.quarantine_reset_time
                tomorrow = now_madrid.date() + timedelta(days=1)
                next_run_datetime_naive = datetime.combine(tomorrow, reset_time)
                next_run_datetime_aware = madrid_tz.localize(next_run_datetime_naive)
                status_msg = f"HIBERNANDO (POOL AGOTADO): No hay claves disponibles. Próxima ejecución: {next_run_datetime_aware.strftime('%Y-%m-%d %H:%M:%S %Z')}."
                if automation_settings.last_run_status != status_msg:
                    _log_structured_event(status_msg, "WARNING")
                    automation_settings.last_run_status = status_msg
                    automation_settings.save(update_fields=['last_run_status'])
                self.retry(eta=next_run_datetime_aware, max_retries=None)
                return
        automation_settings.refresh_from_db()
        zombie_threshold = timezone.now() - timedelta(minutes=5)
        zombie_content_tasks = PendingContentTask.objects.filter(status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.PENDING], updated_at__lt=zombie_threshold)
        for task in zombie_content_tasks:
            message = f"VIGILANTE (CONTENT): Tarea '{task.id}' detectada como ZOMBIE. Marcada para rescate."
            _log_structured_event(message, "WARNING", {"task_id": str(task.id)})
            task.status = PendingContentTask.StatusChoices.FAILED_RETRYABLE
            task.save(update_fields=["status"])
        zombie_assessment_tasks = Assessment.objects.filter(status=Assessment.AssessmentStatus.PROCESSING, created_at__lt=zombie_threshold)
        for task in zombie_assessment_tasks:
            message = f"VIGILANTE (ASSESSMENT): Tarea '{task.id}' detectada como ZOMBIE. Marcada para rescate."
            _log_structured_event(message, "WARNING", {"task_id": str(task.id)})
            task.status = Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE
            task.save(update_fields=["status"])
        assessment_gen_to_rescue = Assessment.objects.filter(status=Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE).order_by('created_at').first()
        if assessment_gen_to_rescue:
            _log_structured_event(f"RESCATE (ASSESSMENT-GEN): Re-encolando la tarea de generación de evaluación {assessment_gen_to_rescue.id}.")
            assessment_gen_to_rescue.status = Assessment.AssessmentStatus.PENDING
            assessment_gen_to_rescue.save(update_fields=["status"])
            generate_assessment_from_content_task.delay(assessment_gen_to_rescue.id)
            return
        assessment_corr_to_rescue = Assessment.objects.filter(status=Assessment.AssessmentStatus.CORRECTION_FAILED_RETRYABLE).order_by('created_at').first()
        if assessment_corr_to_rescue:
            _log_structured_event(f"RESCATE (ASSESSMENT-CORR): Re-encolando la tarea de corrección de evaluación {assessment_corr_to_rescue.id}.")
            correct_assessment_task.delay(assessment_corr_to_rescue.id)
            return
        task_to_rescue = PendingContentTask.objects.filter(status__in=[PendingContentTask.StatusChoices.FAILED_RETRYABLE, PendingContentTask.StatusChoices.FAILED_QUOTA]).order_by('created_at').first()
        if task_to_rescue:
            _log_structured_event(f"RESCATE (CONTENT): Re-encolando la tarea de contenido {task_to_rescue.id}.")
            
            # [FIX V24.5] RESETEO CRÍTICO: Limpiar historial de errores al cambiar de contexto/clave
            # Evita que una clave nueva herede los 'strikes' de la anterior.
            sc = task_to_rescue.structured_content
            if sc.get("consecutive_quota_errors", 0) > 0:
                sc["consecutive_quota_errors"] = 0
                task_to_rescue.structured_content = sc
            
            task_to_rescue.status = PendingContentTask.StatusChoices.PENDING
            task_to_rescue.save(update_fields=["status", "structured_content"])
            generate_full_course_task.delay(str(task_to_rescue.id))
            status_msg = f"AUTO-RECUPERACIÓN: Tarea para '{task_to_rescue}' re-encolada."
            automation_settings.last_run_status = status_msg
            automation_settings.last_run_timestamp = timezone.now()
            automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
            return
        approved_request = ContentRequest.objects.filter(status=ContentRequest.StatusChoices.APPROVED).order_by('created_at').first()
        if approved_request and approved_request.subject.content_materials.count() == 0:
            subject_to_process = approved_request.subject
            origin = PendingContentTask.TaskOrigin.APPROVED_REQUEST
            with transaction.atomic():
                req = ContentRequest.objects.select_for_update().get(id=approved_request.id)
                req.status = ContentRequest.StatusChoices.IN_PROGRESS
                req.save(update_fields=["status"])
            _log_structured_event(f"PRIORIDAD 1 (REQUEST): Reclamada la solicitud para '{subject_to_process.name}'.")
            admin_user = CustomUser.objects.filter(is_superuser=True, is_active=True).order_by('pk').first()
            new_task = PendingContentTask.objects.create(subject=subject_to_process, assigned_to=admin_user, task_origin=origin)
            generate_full_course_task.delay(str(new_task.id))
            status_msg = f"TAREA LANZADA (REQUEST): '{subject_to_process.name}' (ID: {new_task.id})."
            automation_settings.last_run_status = status_msg
            automation_settings.last_run_timestamp = timezone.now()
            automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
            return
        pending_assessment = Assessment.objects.filter(status=Assessment.AssessmentStatus.PENDING).order_by('created_at').first()
        if pending_assessment:
            _log_structured_event(f"PRIORIDAD 2 (ASSESSMENT): Reclamada la evaluación pendiente {pending_assessment.id}.", "INFO")
            generate_assessment_from_content_task.delay(pending_assessment.id)
            status_msg = f"TAREA LANZADA (ASSESSMENT): '{pending_assessment.id}'."
            automation_settings.last_run_status = status_msg
            automation_settings.last_run_timestamp = timezone.now()
            automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
            return
        if PendingContentTask.objects.filter(status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.PENDING]).exists():
            status_msg = "EN ESPERA: Hay tareas de contenido activas. La generación masiva se pospone."
            if automation_settings.last_run_status != status_msg:
                _log_structured_event(status_msg, "INFO")
                automation_settings.last_run_status = status_msg
                automation_settings.save(update_fields=['last_run_status'])
            return
        while True:
            subject_qs = _get_next_subject_queryset(automation_settings)
            subject_to_process = subject_qs.order_by('?').first()
            if subject_to_process:
                admin_user = CustomUser.objects.filter(is_superuser=True, is_active=True).order_by('pk').first()
                if not admin_user:
                    _log_structured_event("CRÍTICO: No se encontró un superusuario para asignar la tarea.", "CRITICAL")
                    raise Exception("No se encontró un superusuario para asignar la tarea.")
                new_task = PendingContentTask.objects.create(subject=subject_to_process, assigned_to=admin_user, task_origin=PendingContentTask.TaskOrigin.MASS_GENERATION)
                log_msg = f"PRIORIDAD 3 (MASS-GEN): Tarea para '{subject_to_process.name}'."
                _log_structured_event(log_msg, "INFO", {"task_id": str(new_task.id)})
                generate_full_course_task.delay(str(new_task.id))
                status_msg = f"TAREA LANZADA (MASS-GEN): '{subject_to_process.name}' (ID: {new_task.id})."
                automation_settings.last_run_status = status_msg
                automation_settings.last_run_timestamp = timezone.now()
                automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
                break
            else:
                filters_were_advanced = _advance_seed_filters_if_needed(automation_settings)
                if filters_were_advanced:
                    _log_structured_event("RE-INTENTO: Lote finalizado, re-intentando encontrar trabajo con filtros más amplios.", "INFO")
                    continue
                else:
                    final_message = "SIN TRABAJO: No quedan más asignaturas para procesar en la configuración actual."
                    _log_structured_event(final_message, "INFO")
                    if automation_settings.last_run_status != final_message:
                         _send_admin_notification("Motor de Automatización en Pausa", final_message)
                         automation_settings.last_run_status = final_message
                         automation_settings.save(update_fields=['last_run_status'])
                    break
    except Exception as e:
        status_msg = f"ERROR CRÍTICO EN BUCLE: {e}"
        _log_structured_event(status_msg, level="CRITICAL", details={"traceback": traceback.format_exc()})
        logger.critical(f"AUTOMATION LOOP: {status_msg}", exc_info=True)
        if 'automation_settings' in locals() and automation_settings:
            automation_settings.last_run_status = status_msg
            automation_settings.save(update_fields=['last_run_status'])
    finally:
        db.close_old_connections()

@shared_task(bind=True, time_limit=21600, acks_late=True, rate_limit='12/m')
def generate_full_course_task(self, task_id: str):
    db.close_old_connections()
    logger.info(f"[V20 REFACTOR] Iniciando Tarea {task_id}, Intento: {self.request.retries + 1}")
    task = None
    api_key = None
    try:
        time.sleep(10)
        automation_settings = AutomationSettings.load()
        api_key = automation_settings.active_api_key
        if not api_key or not api_key.is_enabled or api_key.is_quarantined:
            log_task_event(task_id, f"ESTADO DEL SISTEMA: La clave activa ('{api_key.name if api_key else 'N/A'}') no está disponible. Reintentando en 15 minutos.", is_error=True)
            # [FIX V24.9] Curación: Hard Wait 62s antes de reintentar
            time.sleep(62)
            raise self.retry(countdown=900)
        task = PendingContentTask.objects.select_related('subject__academic_year__degree__branch__university', 'subject__content_hash_family').get(id=task_id)
        if task.subject and task.subject.content_hash_family:
            family = task.subject.content_hash_family
            log_task_event(task_id, f"GUARDIÁN: Verificando Familia de Contenido (Hash: {family.hash[:12]}...) para la asignatura '{task.subject.name}'.")
            if family.content_material:
                existing_material = family.content_material
                log_task_event(task_id, f"GUARDIÁN: La familia ya tiene material existente (ID: {existing_material.id}). Vinculando esta asignatura y finalizando.")
                with transaction.atomic():
                    existing_material.subject.add(task.subject)
                    task_to_complete = PendingContentTask.objects.select_for_update().get(id=task_id)
                    task_to_complete.status = PendingContentTask.StatusChoices.COMPLETED
                    task_to_complete.content_material = existing_material
                    task_to_complete.notes = "Tarea completada por el Guardián de Familia. Se encontró y vinculó contenido preexistente a través de la familia."
                    task_to_complete.save(update_fields=["status", "content_material", "notes", "updated_at"])
                log_task_event(task_id, "GUARDIÁN: Vínculo asegurado y tarea marcada como completada. Ejecución finalizada.")
                return
        if not task.log_file_path:
            log_dir = os.path.join(settings.BASE_DIR, "logs", "content_automation")
            os.makedirs(log_dir, exist_ok=True)
            task.log_file_path = os.path.join(log_dir, f"task_{task_id}.log")
            task.save(update_fields=["log_file_path"])
        log_task_event(task_id, f"Usando clave de API activa: '{api_key.name}'.")
        if task.status in [PendingContentTask.StatusChoices.PENDING, PendingContentTask.StatusChoices.FAILED_RETRYABLE, PendingContentTask.StatusChoices.FAILED_QUOTA]:
            # [FIX V24.6] Tabula Rasa: Al iniciar/reiniciar, el contador de errores DEBE ser 0.
            sc = task.structured_content
            if sc.get("consecutive_quota_errors", 0) > 0:
                sc["consecutive_quota_errors"] = 0
                task.structured_content = sc
                # Guardamos status y contenido estructurado a la vez
                task.status = PendingContentTask.StatusChoices.PROCESSING
                task.save(update_fields=["status", "structured_content"])
                log_task_event(task_id, "Tarea iniciada (Contador reseteado). Estado cambiado a 'Procesando'.")
            else:
                task.status = PendingContentTask.StatusChoices.PROCESSING
                task.save(update_fields=["status"])
                log_task_event(task_id, "Tarea iniciada. Estado cambiado a 'Procesando'.")
        if task.status == PendingContentTask.StatusChoices.PAUSED:
            logger.info(f"Tarea {task_id} está en PAUSA. Re-encolando para futura comprobación.")
            self.retry(countdown=600)
            return
        if not task.structured_content or "master_schema" not in task.structured_content:
            log_task_event(task_id, "Fase de Inicialización: No se encontró plan de trabajo. Generándolo ahora.")
            manual_classification = task.structured_content.get('manual_classification')
            course_title = task.course_title or (task.subject.name if task.subject else "Curso sin título")
            if task.subject:
                topic_description = task.subject.name
                degree = task.subject.academic_year.degree
                academic_context = (f"- Universidad: {degree.branch.university.name}\n- Rama: {degree.branch.name}\n- Titulación: {degree.name} ({degree.get_degree_type_display()})")
                learning_objectives = json.dumps(task.subject.learning_objectives, ensure_ascii=False) if task.subject.learning_objectives else ""
                syllabus = json.dumps(task.subject.course_content_outline, ensure_ascii=False) if task.subject.course_content_outline else ""
            else:
                topic_description = task.prompt_text
                academic_context = ""
                learning_objectives = ""
                syllabus = ""
            metadata_prompt_base = generate_course_metadata_prompt(topic_description, academic_context)
            metadata_prompt = (f"{metadata_prompt_base}\n\n" "IMPORTANTE: Devuelve la respuesta exclusivamente como un bloque de código JSON " "dentro de un bloque ```json ... ```. No incluyas ningún otro texto fuera de este bloque.")
            success, response_text, _ = generate_text_content(metadata_prompt, api_key=api_key, task_id=task_id)
            if not success:
                raise ResourceExhausted(f"Fallo crítico en inicialización al generar metdatos: {response_text}")
            cleaned_json_str = clean_json_response(response_text)
            metadata = json.loads(cleaned_json_str)
            classification_data = metadata.get("clasificacion_intelectual", {})
            if not all(classification_data.get(key) for key in ["categoria_general", "subcategoria", "palabras_clave"]):
                raise ContentGenerationError("Clasificación intelectual inválida o incompleta por parte de la IA.")
            schema_prompt = generate_master_schema_prompt(topic_description, academic_context, learning_objectives, syllabus)
            success, schema_or_error, _ = generate_text_content(schema_prompt, api_key=api_key, task_id=task_id)
            if not success:
                raise ResourceExhausted(f"Fallo crítico en inicialización al generar esquema: {schema_or_error}")
            master_schema_md = schema_or_error
            section_count = len(_parse_master_schema(master_schema_md))
            task.section_count = section_count
            new_structured_content = {"metadata": metadata, "master_schema": master_schema_md, "academic_context": academic_context}
            if manual_classification:
                new_structured_content['manual_classification'] = manual_classification
                log_task_event(task_id, "Clasificación manual del usuario preservada durante la inicialización.")
            task.structured_content = new_structured_content
            task.save(update_fields=["structured_content", "section_count"])
            log_task_event(task_id, f"Plan de trabajo generado y guardado. Secciones: {section_count}.")
        task.refresh_from_db()
        parsed_schema = _parse_master_schema(task.structured_content["master_schema"])
        for index, (_, title) in enumerate(parsed_schema):
            db.close_old_connections()
            order = index + 1
            if GeneratedContentChunk.objects.filter(task=task, order=order).exists():
                continue
            task.refresh_from_db(fields=["status"])
            if task.status == PendingContentTask.StatusChoices.PAUSED:
                log_task_event(task_id, "Tarea pausada por un administrador. Guardando progreso y saliendo.")
                self.retry(countdown=600)
                return
            academic_context = task.structured_content.get("academic_context", "")
            initial_prompt = generate_atomic_content_prompt(course_title=task.course_title or task.subject.name, section_title=title, master_schema=task.structured_content["master_schema"], academic_context=academic_context)
            log_task_event(task_id, f'Procesando sección {order}/{len(parsed_schema)}: "{title}"')
            log_task_event(task_id, "Enviando prompt atómico a la API.")
            success, content_or_error, _ = generate_text_content(initial_prompt, api_key=api_key, task_id=task_id)
            if not success:
                 raise ResourceExhausted(f"Fallo en la generación de la sección: {content_or_error}")
            content_text, sources_text = _parse_markdown_with_separator(content_or_error)
            GeneratedContentChunk.objects.create(task=task, order=order, content=content_text, ai_sources=sources_text)
            log_task_event(task_id, f"Fragmento {order}/{len(parsed_schema)} guardado.")
            # [FIX V24.4] RESETEO INCONDICIONAL (BRUTE FORCE)
            task.refresh_from_db(fields=["structured_content"])
            sc = task.structured_content
            
            # Capturamos valor previo para confirmar en el log si hubo limpieza
            prev_errors = sc.get('consecutive_quota_errors', 0)
            
            # ASIGNACIÓN DIRECTA A CERO SIEMPRE QUE HAYA ÉXITO
            sc["consecutive_quota_errors"] = 0
            task.structured_content = sc
            task.save(update_fields=["structured_content"])
            
            # Solo ensuciamos el log si realmente veníamos de un error, para confirmar el reset
            if prev_errors > 0:
                log_task_event(task_id, f"Recuperado de error de cuota.\nReseteo ejecutado.\nValor anterior: {prev_errors}\nValor actual: {sc['consecutive_quota_errors']}/4")
            # [FIX V24.9] Prevención: 5s entre peticiones
            # [FIX V24.10] Rate Limit: 5s pausa = max 12 RPM (<15 limit)
            time.sleep(5)
        task.refresh_from_db()
        if task.content_chunks.count() == len(parsed_schema):
            log_task_event(task_id, "Ensamblaje final.")
            final_course_title = task.subject.name if task.subject else task.course_title
            final_markdown = _assemble_final_markdown_from_chunks(final_course_title, task.structured_content["metadata"], task.structured_content["master_schema"], list(task.content_chunks.all()))
            log_task_event(task_id, "Iniciando fase de clasificación de contenido.")
            manual_classification = task.structured_content.get('manual_classification')
            
            # [REPARACIÓN] Intentar recuperar clasificación del material vinculado si falta en el JSON
            if not task.subject and not manual_classification and task.content_material:
                log_task_event(task_id, "RECUPERACIÓN: Usando clasificación del Material de Contenido vinculado.")
                manual_classification = {
                    'master_category_id': str(task.content_material.master_category.id),
                    'sub_category_id': str(task.content_material.sub_category.id) if task.content_material.sub_category else None
                }

            if task.subject:
                log_task_event(task_id, "Clasificación académica: Asignando contenido a asignatura oficial.")
                master_category, sub_category = None, None
            elif manual_classification:
                log_task_event(task_id, "Clasificación MANUAL para contenido libre iniciada.")
                master_category = FreeContentMasterCategory.objects.get(id=manual_classification['master_category_id'])
                sub_category = None
                if manual_classification.get('sub_category_id'):
                    sub_category = FreeContentSubCategory.objects.get(id=manual_classification['sub_category_id'])
            else:
                raise ContentGenerationError("Estado de tarea anómalo: Contenido libre sin clasificación manual.")
            with transaction.atomic():
                task_final = PendingContentTask.objects.select_for_update().get(id=task_id)
                is_free = task_final.subject is None
                
                # [FIX DEDUP] Reutilizar material existente si la tarea ya lo tiene vinculado (creado por la vista)
                if task_final.content_material:
                    log_task_event(task_id, f"Actualizando material existente (ID: {task_final.content_material.id}) en lugar de crear uno nuevo.")
                    new_content = task_final.content_material
                    new_content.title = final_course_title
                    new_content.short_description = task_final.structured_content["metadata"].get("descripcion_corta", "")
                    new_content.markdown_content = final_markdown
                    new_content.master_category = master_category
                    new_content.sub_category = sub_category
                    new_content.creator = task_final.assigned_to
                    new_content.is_free_content = is_free
                    new_content.is_public = True  # [FIX] Asegurar visibilidad al finalizar
                    new_content.save()
                else:
                    log_task_event(task_id, "Creando nuevo material de contenido.")
                    new_content = ContentMaterial.objects.create(
                        title=final_course_title, 
                        short_description=task_final.structured_content["metadata"].get("descripcion_corta", ""), 
                        markdown_content=final_markdown, 
                        master_category=master_category, 
                        sub_category=sub_category, 
                        creator=task_final.assigned_to, 
                        is_free_content=is_free,
                        is_public=True  # [FIX] Asegurar visibilidad
                    )
                if not is_free:
                    family = task_final.subject.content_hash_family
                    if family:
                        log_task_event(task_id, f"Vinculando nuevo contenido a la Familia Hash {family.hash[:12]}...")
                        family.content_material = new_content
                        family.save(update_fields=['content_material'])
                        all_subjects_in_family = family.subjects.all()
                        count = all_subjects_in_family.count()
                        new_content.subject.add(*all_subjects_in_family)
                        log_task_event(task_id, f"VINCULACIÓN POR FAMILIA: Contenido vinculado a la familia y a sus {count} asignatura(s) miembro.")
                    else:
                        log_task_event(task_id, f"ADVERTENCIA: La asignatura '{task_final.subject.name}' no tiene familia. Vinculando solo a esta asignatura.", "WARNING")
                        new_content.subject.add(task_final.subject)
                else:
                    log_task_event(task_id, "Contenido libre creado, no se vincula a ninguna asignatura académica.")
                task_final.content_material = new_content
                task_final.status = PendingContentTask.StatusChoices.COMPLETED
                task_final.save(update_fields=["status", "content_material"])
            _send_completion_notifications(new_content)
        else:
            raise ContentGenerationError("Proceso incompleto, no se generaron todas las secciones.")
    except ResourceExhausted as e:
        if task and api_key:
            # [FIX V24.1] Lógica de Cuota Inteligente: Solo cuarentena si los fallos son CONSECUTIVOS
            task.refresh_from_db()
            sc = task.structured_content
            # Inicializar si no existe
            current_consecutive_fails = sc.get('consecutive_quota_errors', 0) + 1
            sc["consecutive_quota_errors"] = current_consecutive_fails
            task.structured_content = sc
            task.save(update_fields=["structured_content"])

            # Umbral de tolerancia (4 intentos consecutivos fallidos = Bloqueo real)
            max_consecutive_fails = 4
            
            if current_consecutive_fails >= max_consecutive_fails:
                log_task_event(task.id, f"CUOTA DIARIA CONFIRMADA: {current_consecutive_fails} fallos CONSECUTIVOS en la misma sección.", is_error=True)
                
                # A. Cuarentena
                api_key.is_quarantined = True
                api_key.save(update_fields=["is_quarantined"])
                _request_quarantine_via_mailbox(api_key)
                
                # B. Marcar tarea
                task.status = PendingContentTask.StatusChoices.FAILED_QUOTA
                task.last_error = f"Cuota agotada en clave {api_key.name} tras {current_consecutive_fails} intentos seguidos."
                task.save(update_fields=["status", "last_error"])
                return

            else:
                log_task_event(task.id, f"Posible error de cuota diaria\nIntento {current_consecutive_fails}/4")
                # Usamos un max_retries infinito en Celery para que no mate la tarea, 
                # ya que el control real lo hacemos nosotros con current_consecutive_fails
                # [FIX V24.10] Hard Wait (62s) por Timezone Skew
                time.sleep(62)
                raise self.retry(exc=e, countdown=70, max_retries=None)
    except Exception as e:
        if task:
            error_traceback = traceback.format_exc()
            logger.critical(f"TRACEBACK CAPTURADO PARA TAREA {task.id}:\n{error_traceback}")
            log_task_event(task.id, f"Error en la tarea: {str(e)}", is_error=True)
            
            # Identificar si es un error recuperable (transitorio) o fatal (código/lógica)
            is_transient = isinstance(e, (TimeoutError, ConnectionError, OSError))
            
            try:
                if is_transient:
                    task.status = PendingContentTask.StatusChoices.FAILED_RETRYABLE
                    task.last_error = f"Error Transitorio: {str(e)}\n{error_traceback}"
                    task.save(update_fields=["status", "last_error"])
                    # Reintentar con backoff
                    self.retry(exc=e, countdown=300, max_retries=5)
                else:
                    # Errores de lógica (TypeError, ValueError, etc) no se arreglan solos.
                    # Fallo fatal inmediato para no bloquear la cola.
                    task.status = PendingContentTask.StatusChoices.FAILED_FATAL
                    task.notes = f"Fallo Fatal por Error de Código/Lógica: {str(e)}"
                    task.last_error = error_traceback
                    task.save(update_fields=["status", "notes", "last_error"])
                    _send_admin_notification("Tarea Fallida Permanentemente (Error Lógico)", f"La tarea para '{task}' ha fallado por un error no recuperable: {str(e)}")
            
            except self.MaxRetriesExceededError:
                logger.critical(f"Máximo de reintentos alcanzado para la tarea {task.id}. Marcando como FATAL.")
                task.status = PendingContentTask.StatusChoices.FAILED_FATAL
                task.notes = f"Falló permanentemente tras reintentos. Error final: {str(e)}"
                task.last_error = error_traceback
                task.save(update_fields=["status", "notes", "last_error"])
                _send_admin_notification("Tarea Fallida Permanentemente", f"La tarea para '{task}' ha fallado tras múltiples reintentos.")
        else:
            logger.critical(f"Error irrecuperable en tarea con ID {task_id} donde 'task' es None: {e}", exc_info=True)

    finally:
        db.close_old_connections()

@shared_task(bind=True, acks_late=True, max_retries=3, default_retry_delay=60)
def generate_assessment_from_content_task(self, assessment_id):
    # Log inicial (usando el nuevo helper para probarlo inmediatamente)
    log_assessment_task_event(assessment_id, f"TAREA GENERACIÓN: Inicio ejecución v{self.request.retries + 1}.")
    
    automation_settings = AutomationSettings.load()
    if not automation_settings.is_running:
        log_assessment_task_event(assessment_id, "Orquestador detenido. Reintentando...", level="WARNING")
        raise self.retry(countdown=300)
    
    assessment = None
    try:
        # 1. Validación de Estado y Bloqueo Inicial
        with transaction.atomic():
            assessment = Assessment.objects.select_for_update().get(pk=assessment_id)
            if assessment.status == Assessment.AssessmentStatus.PAUSED:
                raise self.retry(countdown=60)
            if assessment.status not in [Assessment.AssessmentStatus.PENDING, Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE, Assessment.AssessmentStatus.PROCESSING]:
                return f"Tarea omitida. Estado: {assessment.get_status_display()}."
            
            # Cambiar a PROCESSING
            assessment.status = Assessment.AssessmentStatus.PROCESSING
            # Limpiar preguntas previas si es reintento
            assessment.questions.all().delete()
            assessment.save(update_fields=["status"])
        
        log_assessment_task_event(assessment_id, "Estado establecido a PROCESSING. Preparando prompt.")

        # 2. Preparación de Datos (Lectura sin bloqueo)
        # Re-leemos para asegurar frescura fuera del lock
        assessment = Assessment.objects.get(pk=assessment_id)
        original_content = assessment.content_copy.original_content
        full_content = original_content.get_full_markdown_content()
        
        if not full_content or not full_content.strip():
            raise ValueError("El contenido para la evaluación está vacío.")
        
        prompt_format_instructions = ("**FORMATO DE SALIDA OBLIGATORIO:**\n" "Cada par pregunta-respuesta DEBE seguir esta estructura exacta, usando los separadores como se indica:\n" "[---PREGUNTA---]\n" "Aquí el texto completo de la pregunta.\n" "[---RESPUESTA---]\n" "Aquí el texto completo de la respuesta modelo.\n" "[---FIN-PREGUNTA---]\n\n")
        prompt = (f"Tu tarea es crear un examen basado en el siguiente texto, cubriendo sus conceptos clave.\n\n" f"{prompt_format_instructions}\n\n" f"Material de estudio:\n---\n{full_content}\n---")
        
        api_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).first()
        if not api_key:
            raise ValueError("No se encontró una clave de API activa.")
        
        log_assessment_task_event(assessment_id, f"Enviando prompt a API (Clave: {api_key.name})...")
        
        success, response_text, _ = generate_text_content(prompt, api_key=api_key)
        if not success:
            raise AIServiceCriticalError(f"API Error: {response_text}")
        
        questions_data = _parse_assessment_text(response_text)
        
        if not questions_data:
            raise ValueError("La IA no devolvió preguntas válidas.")
            
        log_assessment_task_event(assessment_id, f"IA devolvió {len(questions_data)} preguntas. Iniciando persistencia.")

        # 3. Persistencia Iterativa (Patrón PAIR: Crear -> Loggear -> Repetir)
        # Actualizamos el total esperado primero
        with transaction.atomic():
            a = Assessment.objects.select_for_update().get(pk=assessment_id)
            a.total_questions_expected = len(questions_data)
            a.questions_processed = 0
            a.save(update_fields=['total_questions_expected', 'questions_processed'])

        for index, q_data in enumerate(questions_data, 1):
            # Paso A: Crear Pregunta (Atómico)
            with transaction.atomic():
                # Obtenemos lock para consistencia padre-hijo
                parent = Assessment.objects.select_for_update().get(pk=assessment_id)
                Question.objects.create(assessment=parent, **q_data)
                parent.questions_processed = index
                parent.save(update_fields=['questions_processed'])
            
            # Paso B: Loggear (Independiente y seguro, usando el helper)
            log_assessment_task_event(assessment_id, f"Pregunta {index}/{len(questions_data)} persistida.")
        
        # 4. Finalización
        with transaction.atomic():
            final_assessment = Assessment.objects.select_for_update().get(pk=assessment_id)
            final_assessment.status = Assessment.AssessmentStatus.COMPLETED
            final_assessment.last_error = None
            final_assessment.save(update_fields=['status', 'last_error', 'expiration_date', 'results_expiration_date'])
        
        log_assessment_task_event(assessment_id, "Proceso completado con ÉXITO.", level="SUCCESS")

        # 5. Notificación (Best Effort)
        try:
            action_url = settings.BASE_URL + reverse("assessment:take_assessment", kwargs={"pk": assessment_id})
            context = {"assessment_pk": assessment_id, "content_title": original_content.title, "action_url": action_url}
            send_unified_notification(user=assessment.user, subject_template="assessment/email/assessment_ready_subject.txt", body_template_prefix="assessment/email/assessment_ready_body", context=context)
        except Exception as e:
            logger.error(f"Fallo en notificación post-generación: {e}")

    except ResourceExhausted as e:
        log_assessment_task_event(assessment_id, f"Error de Cuota: {e}", level="ERROR")
        if assessment:
            with transaction.atomic():
                a = Assessment.objects.select_for_update().get(pk=assessment_id)
                a.status = Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE
                a.last_error = str(e)
                a.save(update_fields=["status", "last_error"])
        # Reintentar si corresponde...
        if "429" in str(e) and self.request.retries < self.max_retries:
             # [FIX V24.8] Hard Wait (61s) para garantizar enfriamiento API
             time.sleep(61)
             raise self.retry(exc=e, countdown=60)

    except Exception as e:
        error_msg = f"Error Fatal: {str(e)}\n{traceback.format_exc()}"
        log_assessment_task_event(assessment_id, error_msg, level="ERROR")
        logger.critical(f"Assessment Task Failed: {e}", exc_info=True)
        if assessment:
            try:
                with transaction.atomic():
                    a = Assessment.objects.select_for_update().get(pk=assessment_id)
                    a.status = Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE
                    a.last_error = str(e)
                    a.save(update_fields=["status", "last_error"])
                self.retry(exc=e)
            except Exception:
                # Si falla el retry o update, fallback final
                Assessment.objects.filter(pk=assessment_id).update(status=Assessment.AssessmentStatus.FAILED_FATAL)

@shared_task(bind=True, acks_late=True, max_retries=3, default_retry_delay=60)
def correct_assessment_task(self, assessment_id):
    _log_assessment_event(assessment_id, "CORRECTION_TASK: Inicio del proceso de corrección.")
    automation_settings = AutomationSettings.load()
    if not automation_settings.is_running:
        log_timestamp(f"CORRECTION_TASK: Orquestador global detenido. Reintentando en 5 min. ID: {assessment_id}")
        raise self.retry(countdown=300)
    assessment = None
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
        if assessment.status == Assessment.AssessmentStatus.PAUSED:
            log_timestamp(f"CORRECTION_TASK: Tarea en PAUSA. Reintentando en 1 min. ID: {assessment_id}")
            raise self.retry(countdown=60)
        user_answers = UserAnswer.objects.filter(question__assessment=assessment).select_related("question")
        if not user_answers.exists():
            assessment.status = Assessment.AssessmentStatus.COMPLETED
            assessment.save(update_fields=["status"])
            return
        with transaction.atomic():
            assessment_to_update = Assessment.objects.select_for_update().get(pk=assessment_id)
            if assessment_to_update.status not in [Assessment.AssessmentStatus.AWAITING_CORRECTION, Assessment.AssessmentStatus.CORRECTING, Assessment.AssessmentStatus.CORRECTION_FAILED_RETRYABLE]:
                 return f"Tarea de corrección omitida. Estado: {assessment_to_update.get_status_display()}."
            assessment_to_update.status = Assessment.AssessmentStatus.CORRECTING
            assessment_to_update.total_questions_expected = user_answers.count()
            assessment_to_update.save(update_fields=["status", "total_questions_expected"])
        app_settings = AssessmentSettings.get_settings()
        expiration_date = timezone.now() + timedelta(days=app_settings.results_expiration_days)
        prompt_format_instructions = ("**FORMATO DE SALIDA OBLIGATORIO:**\n" "PUNTUACION: [Un número entero de 0 a 100]\n" "FEEDBACK: [Tu feedback constructivo detallado]")
        api_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).first()
        if not api_key:
            raise ValueError("No se encontró una clave de API activa.")
        
        answers_to_correct = user_answers.filter(score__isnull=True)
        # Actualizar progreso inicial
        initial_processed = user_answers.count() - answers_to_correct.count()
        Assessment.objects.filter(pk=assessment_id).update(questions_processed=initial_processed)

        for i, answer in enumerate(answers_to_correct, 1):
            assessment.refresh_from_db(fields=['status'])
            if assessment.status == Assessment.AssessmentStatus.PAUSED:
                log_timestamp(f"CORRECTION_TASK: Tarea pausada durante la corrección. ID: {assessment_id}")
                raise self.retry(countdown=60)
            
            if not answer.answer_text:
                Assessment.objects.filter(pk=assessment_id).update(questions_processed=F("questions_processed") + 1)
                continue

            prompt = (f"Evalúa la siguiente respuesta de un usuario, comparándola con la pregunta y la respuesta modelo.\n\n" f'Pregunta: "{answer.question.question_text}"\n' f'Respuesta Modelo: "{answer.question.model_answer}"\n' f'Respuesta del Usuario: "{answer.answer_text}"\n\n' f"{prompt_format_instructions}")
            
            # Log antes de la llamada
            _log_assessment_event(assessment_id, f"Corrigiendo respuesta {i}/{answers_to_correct.count()}...")
            
            success, response_text, _ = generate_text_content(prompt, api_key=api_key)
            if not success:
                raise AIServiceCriticalError(f"API falló para UserAnswer ID {answer.id}: {response_text}")
            
            correction = _parse_correction_text(response_text)
            
            with transaction.atomic():
                if correction and correction.get("score") is not None:
                    answer.score = correction["score"]
                    answer.feedback = correction["feedback"]
                    answer.correction_expiration_date = expiration_date
                    answer.save(update_fields=["score", "feedback", "correction_expiration_date"])
                
                # Actualizar contador de progreso en Assessment
                Assessment.objects.filter(pk=assessment_id).update(questions_processed=F("questions_processed") + 1)
            
            time.sleep(2)

        # [V2 RESILIENCIA] Notificación desacoplada de la transacción final.
        should_notify = False
        assessment_user = None
        content_title_val = None
        
        with transaction.atomic():
            assessment_to_complete = Assessment.objects.select_for_update().get(pk=assessment_id)
            if assessment_to_complete.questions_processed >= assessment_to_complete.total_questions_expected:
                assessment_to_complete.status = Assessment.AssessmentStatus.RESULTS_AVAILABLE
                assessment_to_complete.results_expiration_date = expiration_date
                assessment_to_complete.save(update_fields=["status", "results_expiration_date"])
                _log_assessment_event(assessment_id, "CORRECTION_TASK: Corrección finalizada y resultados disponibles.", "SUCCESS")
                
                should_notify = True
                assessment_user = assessment_to_complete.user
                content_title_val = assessment_to_complete.content_copy.original_content.title

        # Notificación
        if should_notify:
            try:
                action_url = settings.BASE_URL + reverse("assessment:view_results", kwargs={"pk": assessment_id})
                context = {"assessment_pk": assessment_id, "content_title": content_title_val, "action_url": action_url}
                send_unified_notification(user=assessment_user, subject_template="assessment/email/results_ready_subject.txt", body_template_prefix="assessment/email/results_ready_body", context=context)
            except Exception as e:
                logger.error(f"CORRECTION_TASK: Corrección finalizada pero falló notificación para ID {assessment_id}: {e}")
    except (AIServiceCriticalError) as e:
        logger.error(f"CORRECTION_TASK: ERROR RECUPERABLE para Assessment ID {assessment_id}: {e}", exc_info=False)
        if assessment:
            assessment.status = Assessment.AssessmentStatus.CORRECTION_FAILED_RETRYABLE
            assessment.last_error = traceback.format_exc()
            assessment.save(update_fields=["status", "last_error"])
        raise self.retry(exc=e)
    except Exception as e:
        logger.critical(f"CORRECTION_TASK: ERROR FATAL/INESPERADO para Assessment ID {assessment_id}: {e}", exc_info=True)
        if assessment:
            try:
                self.retry(exc=e)
            except MaxRetriesExceededError:
                assessment.status = Assessment.AssessmentStatus.FAILED_FATAL
                assessment.last_error = traceback.format_exc()
                assessment.save(update_fields=["status", "last_error"])

@shared_task(name="orchestrator.tasks.expire_untaken_assessments")
def expire_untaken_assessments():
    now = timezone.now()
    expiration_limit = getattr(settings, "ASSESSMENT_EXPIRATION_SECONDS", 86400)
    expiration_threshold = now - timedelta(seconds=expiration_limit)
    log_timestamp(f"EXPIRE_UNTAKEN_TASK: Buscando evaluaciones 'COMPLETED' creadas antes de {expiration_threshold}.")
    assessments_to_expire = Assessment.objects.filter(status="COMPLETED", created_at__lt=expiration_threshold)
    count = assessments_to_expire.count()
    if count == 0:
        return "No hay evaluaciones no realizadas para expirar."
    updated_rows = assessments_to_expire.update(status="EXPIRED_UNTAKEN")
    log_timestamp(f"EXPIRE_UNTAKEN_TASK: Se han hecho caducar {updated_rows} evaluaciones.")
    return f"Se han marcado como caducadas {updated_rows} evaluaciones."

@shared_task(name="orchestrator.tasks.purge_and_penalize_corrections")
def purge_and_penalize_corrections():
    now = timezone.now()
    log_timestamp(f"PURGE_PENALIZE_TASK: Buscando correcciones caducadas antes de {now}.")
    expired_assessments = Assessment.objects.filter(status="RESULTS_AVAILABLE", results_expiration_date__lt=now).distinct()
    if not expired_assessments.exists():
        return "No hay correcciones para procesar."
    assessments_to_penalize = expired_assessments.filter(was_viewed=False)
    penalized_count = assessments_to_penalize.update(status="CORRECTION_EXPIRED")
    if penalized_count > 0:
        log_timestamp(f"PURGE_PENALIZE_TASK: Penalizadas {penalized_count} evaluaciones no vistas.")
    answers_to_purge = UserAnswer.objects.filter(question__assessment__in=expired_assessments, score__isnull=False)
    purged_count = answers_to_purge.update(score=None, feedback="La corrección y el feedback de esta respuesta han caducado.")
    if purged_count > 0:
        log_timestamp(f"PURGE_PENALIZE_TASK: Purgado el contenido de {purged_count} respuestas.")
    return f"Tarea completada. Penalizadas: {penalized_count}. Purgadas: {purged_count}."
