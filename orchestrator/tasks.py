# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/tasks.py
import logging
import traceback
import os
import json
import dirtyjson
import time
import re
from datetime import datetime, timedelta
import pytz

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError, Retry
from django import db
from django.db import transaction, OperationalError, InterfaceError
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
from contents.services.navigation_builder import refresh_user_navigation
from contents.models import (
    ContentMaterial,
    FreeContentMasterCategory,
    FreeContentSubCategory,
)
from core.services.gemini_service import generate_text_content, clean_json_response, AIServiceCriticalError

from core.services.prompt_generators import (
    generate_course_metadata_prompt,
    generate_master_schema_prompt,
    generate_atomic_content_prompt
)
from messaging.push_utils import send_notification_to_user
from core.utils import send_unified_notification

logger = logging.getLogger(__name__)
User = get_user_model()

# [ARQUITECTURA] Rutas absolutas gestionadas por settings
QUARANTINE_MAILBOX_FILE = os.path.join(settings.BASE_DIR, "quarantine_requests.log")

# ==============================================================================
# SECCIÓN 1: FUNCIONES AUXILIARES DEL ORQUESTADOR
# ==============================================================================

def _log_structured_event(message: str, level: str = "INFO", details: dict = None):
    try:
        settings_obj = AutomationSettings.load()
        log_entry = {
            "timestamp": timezone.now().isoformat(),
            "level": level,
            "message": message,
            "details": details or {}
        }
        settings_obj.event_log.insert(0, log_entry)
        settings_obj.event_log = settings_obj.event_log[:100]
        settings_obj.save(update_fields=['event_log'])
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
        automation_settings = AutomationSettings.load()
        threshold = timezone.now() - timedelta(hours=automation_settings.zombie_task_threshold_hours)
        
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
            zombies.delete()
            _log_structured_event(f"LIMPIEZA AUTOMÁTICA: Se han eliminado {count} tareas residuales inactivas por >24h.", "WARNING")
    except Exception as e:
        logger.error(f"Error en limpieza de zombies: {e}")

def _get_next_subject_queryset(settings_obj):
    base_queryset = Subject.objects.filter(content_materials__isnull=True)
    active_task_subject_names = PendingContentTask.objects.exclude(
        status__in=[PendingContentTask.StatusChoices.COMPLETED, PendingContentTask.StatusChoices.FAILED_FATAL]
    ).values_list('subject__name', flat=True).distinct()
    query = base_queryset.exclude(name__in=active_task_subject_names)
    if settings_obj.seed_branch:
        query = query.filter(academic_year__degree__branch=settings_obj.seed_branch)
    if settings_obj.seed_degree:
        query = query.filter(academic_year__degree=settings_obj.seed_degree)
    if settings_obj.seed_year:
        try:
            year_map = {"Primero": 1, "Segundo": 2, "Tercero": 3, "Cuarto": 4, "Quinto": 5}
            year_int = year_map.get(settings_obj.seed_year)
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
    separator_pattern = r"(?i:^[-*_#]*\s*(?:FUENTES|BIBLIOGRAF[ÍI]A|REFERENCIAS)\s*[-*_#]*$)"
    matches = list(re.finditer(separator_pattern, raw_text, re.MULTILINE))
    if matches:
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
# SECCIÓN 3: TAREAS CELERY
# ==============================================================================

class ContentGenerationError(Exception):
    pass

@shared_task(bind=True)
def global_orchestrator_task(self):
    try:
        try:
            settings_check = AutomationSettings.load()
            if settings_check.last_run_timestamp:
                delta = timezone.now() - settings_check.last_run_timestamp
                if delta.total_seconds() < 45:
                    logger.warning(f'ORCHESTRATOR DEBOUNCE: Ejecución omitida (Delta: {delta.total_seconds():.1f}s < 45s). Drenando cola.')
                    return
        except Exception:
            pass 

        _purge_zombie_tasks()
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
        if active_key:
            active_key.refresh_from_db()
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
        

        task_to_rescue = PendingContentTask.objects.filter(status__in=[PendingContentTask.StatusChoices.FAILED_RETRYABLE, PendingContentTask.StatusChoices.FAILED_QUOTA]).order_by('created_at').first()
        if task_to_rescue:
            _log_structured_event(f"RESCATE (CONTENT): Re-encolando la tarea de contenido {task_to_rescue.id}.")
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
        

        if PendingContentTask.objects.filter(status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.PENDING]).exists():
            status_msg = "EN ESPERA: Hay tareas de contenido activas. La generación masiva se pospone."
            if automation_settings.last_run_status != status_msg:
                _log_structured_event(status_msg, "INFO")
                automation_settings.last_run_status = status_msg
                automation_settings.save(update_fields=['last_run_status'])
            return
        if not automation_settings.is_mass_generation_enabled:
            status_msg = "AHORRO DE ENERGÍA: Generación masiva desactivada. A la espera de solicitudes manuales."
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
    except (Retry, MaxRetriesExceededError):
        raise
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
def generate_full_course_task(self, task_id):
    db.close_old_connections()
    logger.info(f"[V24.13 ULTRA-BLINDADO] Iniciando Tarea {task_id}.")
    task = None
    api_key = None
    try:
        time.sleep(2)
        automation_settings = AutomationSettings.load()
        api_key = automation_settings.active_api_key
        
        if not api_key or not api_key.is_enabled or api_key.is_quarantined:
             next_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
             if next_key:
                 automation_settings.active_api_key = next_key
                 automation_settings.save(update_fields=['active_api_key'])
                 api_key = next_key
             else:
                 log_task_event(task_id, "HIBERNACIÓN: No hay claves disponibles al inicio.", is_error=True)
                 time.sleep(60)
                 raise self.retry(countdown=900)

        task = PendingContentTask.objects.select_related('subject__academic_year__degree__branch__university', 'subject__content_hash_family').get(id=task_id)
        
        if task.status == PendingContentTask.StatusChoices.FAILED_FATAL:
            logger.warning(f"DRENAJE: Tarea {task_id} ya es FATAL. Omitiendo ejecución para vaciar cola.")
            return

        PendingContentTask.objects.filter(id=task_id).update(global_actuation_count=F('global_actuation_count') + 1)
        task.refresh_from_db(fields=['global_actuation_count'])
        
        limit_actuations = automation_settings.max_task_actuations
        if task.global_actuation_count > limit_actuations:
            msg = f"FUSIBLE FUNDIDO: {task.global_actuation_count}/{limit_actuations}."
            log_task_event(task_id, msg, is_error=True)
            task.status = PendingContentTask.StatusChoices.FAILED_FATAL
            task.notes = f"{task.notes} | {msg}"
            task.save(update_fields=["status", "notes"])
            return

        if not task.log_file_path:
            log_dir = os.path.join(settings.BASE_DIR, "logs", "content_automation")
            os.makedirs(log_dir, exist_ok=True)
            task.log_file_path = os.path.join(log_dir, f"task_{task_id}.log")
            task.save(update_fields=["log_file_path"])

        if task.status in [PendingContentTask.StatusChoices.PENDING, PendingContentTask.StatusChoices.FAILED_RETRYABLE, PendingContentTask.StatusChoices.FAILED_QUOTA]:
            task.status = PendingContentTask.StatusChoices.PROCESSING
            task.save(update_fields=["status"])
            log_task_event(task_id, "Tarea iniciada (Status -> PROCESSING).")

        if not task.structured_content or "master_schema" not in task.structured_content:
            log_task_event(task_id, "Generando Plan de Trabajo...")
            while True: 
                task.refresh_from_db(fields=["status"])
                if task.status == PendingContentTask.StatusChoices.PAUSED:
                    log_task_event(task_id, "PAUSA ADMIN DETECTADA.")
                    self.retry(countdown=600)
                    return

                automation_settings = AutomationSettings.load()
                api_key = automation_settings.active_api_key
                if not api_key or not api_key.is_enabled or api_key.is_quarantined:
                     api_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
                     if api_key:
                         automation_settings.active_api_key = api_key
                         automation_settings.save(update_fields=['active_api_key'])
                     else:
                         log_task_event(task_id, "SIN CLAVES (INIT). Esperando...", is_error=True)
                         time.sleep(300)
                         continue

                course_title = task.course_title or (task.subject.name if task.subject else "Curso sin título")
                if task.subject:
                    topic_description = task.subject.name
                    degree = task.subject.academic_year.degree
                    academic_context = (f"- Universidad: {degree.branch.university.name}\n- Rama: {degree.branch.name}\n- Titulación: {degree.name}")
                    learning_objectives = json.dumps(task.subject.learning_objectives, ensure_ascii=False) if task.subject.learning_objectives else ""
                    syllabus = json.dumps(task.subject.course_content_outline, ensure_ascii=False) if task.subject.course_content_outline else ""
                else:
                    topic_description = task.prompt_text
                    academic_context = ""
                    learning_objectives = ""
                    syllabus = ""
                    
                metadata_prompt = generate_course_metadata_prompt(topic_description, academic_context) + "\n\nJSON Only."
                
                try:
                    success, response_text, _ = generate_text_content(metadata_prompt, api_key=api_key, task_id=task_id)
                except Exception as ex:
                    success = False
                    response_text = str(ex)

                if not success:
                    error_str = str(response_text)
                    is_quota = "429" in error_str or "Resource" in error_str or "Quota" in error_str or "503" in error_str or "overloaded" in error_str
                    if is_quota:
                        api_key.refresh_from_db()
                        api_key.consecutive_failures += 1
                        api_key.save(update_fields=["consecutive_failures"])
                        if api_key.consecutive_failures >= 4:
                            api_key.is_quarantined = True
                            api_key.save(update_fields=["is_quarantined"])
                            _request_quarantine_via_mailbox(api_key)
                            next_k = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).exclude(id=api_key.id).first()
                            if next_k:
                                automation_settings.active_api_key = next_k
                                automation_settings.save(update_fields=['active_api_key'])
                                log_task_event(task_id, f"ROTACIÓN (INIT): Nueva clave {next_k.name}.")
                            else:
                                log_task_event(task_id, "POOL AGOTADO TRAS ROTACIÓN. Esperando...", is_error=True)
                                time.sleep(60)
                        else:
                            log_task_event(task_id, f"STRIKE INIT {api_key.consecutive_failures}/4. Esperando 60s...", is_error=True)
                            time.sleep(60)
                        continue 
                    else:
                        log_task_event(task_id, f"ERROR INIT NO-CUOTA: {error_str}. Reintentando en 30s...", is_error=True)
                        time.sleep(30)
                        continue

                cleaned_json_str = clean_json_response(response_text)
                metadata = json.loads(cleaned_json_str)
                schema_prompt = generate_master_schema_prompt(topic_description, academic_context, learning_objectives, syllabus)
                
                try:
                    success, schema_or_error, _ = generate_text_content(schema_prompt, api_key=api_key, task_id=task_id)
                except Exception as ex:
                    success = False
                    schema_or_error = str(ex)
                
                if not success:
                    error_str = str(schema_or_error)
                    is_quota = "429" in error_str or "Resource" in error_str or "Quota" in error_str or "503" in error_str or "overloaded" in error_str
                    if is_quota:
                        api_key.refresh_from_db()
                        api_key.consecutive_failures += 1
                        api_key.save(update_fields=["consecutive_failures"])
                        if api_key.consecutive_failures >= 4:
                            api_key.is_quarantined = True
                            api_key.save(update_fields=["is_quarantined"])
                            _request_quarantine_via_mailbox(api_key)
                            next_k = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).exclude(id=api_key.id).first()
                            if next_k:
                                automation_settings.active_api_key = next_k
                                automation_settings.save(update_fields=['active_api_key'])
                                log_task_event(task_id, f"ROTACIÓN (INIT): Nueva clave {next_k.name}.")
                            else:
                                time.sleep(60)
                        else:
                            log_task_event(task_id, f"STRIKE INIT {api_key.consecutive_failures}/4. Esperando 60s...", is_error=True)
                            time.sleep(60)
                        continue 
                    else:
                        log_task_event(task_id, f"ERROR INIT ESQUEMA NO-CUOTA: {error_str}. Reintentando en 30s...", is_error=True)
                        time.sleep(30)
                        continue
                
                if api_key.consecutive_failures > 0:
                    api_key.consecutive_failures = 0
                    api_key.save(update_fields=['consecutive_failures'])

                master_schema_md = schema_or_error
                section_count = len(_parse_master_schema(master_schema_md))
                
                new_structured_content = {"metadata": metadata, "master_schema": master_schema_md, "academic_context": academic_context}
                if task.structured_content.get('manual_classification'):
                    new_structured_content['manual_classification'] = task.structured_content['manual_classification']
                    
                task.section_count = section_count
                task.structured_content = new_structured_content
                task.save(update_fields=["structured_content", "section_count"])
                log_task_event(task_id, f"Plan generado: {section_count} secciones.")
                break 

        task.refresh_from_db()
        parsed_schema = _parse_master_schema(task.structured_content["master_schema"])
        
        for index, (_, title) in enumerate(parsed_schema):
            db.close_old_connections()
            order = index + 1
            if GeneratedContentChunk.objects.filter(task=task, order=order).exists():
                continue

            while True:
                task.refresh_from_db(fields=["status"])
                if task.status == PendingContentTask.StatusChoices.PAUSED:
                    log_task_event(task_id, "PAUSA ADMIN DETECTADA.")
                    self.retry(countdown=600)
                    return

                automation_settings = AutomationSettings.load()
                api_key = automation_settings.active_api_key
                if not api_key or not api_key.is_enabled or api_key.is_quarantined:
                     api_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
                     if api_key:
                         automation_settings.active_api_key = api_key
                         automation_settings.save(update_fields=['active_api_key'])
                     else:
                         log_task_event(task_id, "SIN CLAVES. Esperando...", is_error=True)
                         time.sleep(300)
                         continue

                academic_context = task.structured_content.get("academic_context", "")
                initial_prompt = generate_atomic_content_prompt(
                    course_title=task.course_title or task.subject.name, 
                    section_title=title, 
                    master_schema=task.structured_content["master_schema"], 
                    academic_context=academic_context
                )
                log_task_event(task_id, f'Generando {order}/{len(parsed_schema)}: "{title}" (Key: {api_key.name})')

                try:
                    success, content_or_error, _ = generate_text_content(initial_prompt, api_key=api_key, task_id=task_id)
                except Exception as ex:
                    success = False
                    content_or_error = str(ex)

                if success:
                    content_text, sources_text = _parse_markdown_with_separator(content_or_error)
                    GeneratedContentChunk.objects.create(task=task, order=order, content=content_text, ai_sources=sources_text)
                    log_task_event(task_id, f"Sección {order} guardada OK.")
                    if api_key.consecutive_failures > 0:
                        log_task_event(task_id, f"CLAVE RECUPERADA: {api_key.name} (Reset contador).")
                        api_key.consecutive_failures = 0
                        api_key.save(update_fields=['consecutive_failures'])
                    time.sleep(5)
                    break 

                else:
                    error_str = str(content_or_error)
                    is_quota = "429" in error_str or "Resource" in error_str or "Quota" in error_str or "503" in error_str or "overloaded" in error_str
                    if is_quota:
                        api_key.refresh_from_db()
                        api_key.consecutive_failures += 1
                        api_key.save(update_fields=["consecutive_failures"])
                        fails = api_key.consecutive_failures
                        if fails >= 4:
                            log_task_event(task_id, f"CLAVE AGOTADA ({fails} fallos): {api_key.name}. Rotando...", is_error=True)
                            api_key.is_quarantined = True
                            api_key.save(update_fields=["is_quarantined"])
                            _request_quarantine_via_mailbox(api_key)
                            next_k = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).exclude(id=api_key.id).first()
                            if next_k:
                                automation_settings.active_api_key = next_k
                                automation_settings.save(update_fields=['active_api_key'])
                                log_task_event(task_id, f"ROTACIÓN OK: Nueva clave {next_k.name}.")
                            else:
                                log_task_event(task_id, "POOL AGOTADO TRAS ROTACIÓN. Esperando...", is_error=True)
                                time.sleep(60)
                        else:
                            log_task_event(task_id, f"STRIKE {fails}/4 ({api_key.name}). Esperando 60s...", is_error=True)
                            time.sleep(60)
                    else:
                        log_task_event(task_id, f"ERROR CHUNK NO-CUOTA: {error_str}. Reintentando en 30s.", is_error=True)
                        time.sleep(30)

        task.refresh_from_db()
        if task.content_chunks.count() >= len(parsed_schema):
            log_task_event(task_id, "Ensamblando curso final...")
            final_course_title = task.subject.name if task.subject else task.course_title
            final_markdown = _assemble_final_markdown_from_chunks(final_course_title, task.structured_content["metadata"], task.structured_content["master_schema"], list(task.content_chunks.all()))
            
            master_category, sub_category = None, None
            manual = task.structured_content.get('manual_classification')
            if task.subject: pass 
            elif manual:
                try:
                    master_category = FreeContentMasterCategory.objects.get(id=manual['master_category_id'])
                    if manual.get('sub_category_id'): sub_category = FreeContentSubCategory.objects.get(id=manual['sub_category_id'])
                except: pass
            
            with transaction.atomic():
                task_final = PendingContentTask.objects.select_for_update().get(id=task_id)
                is_free = task_final.subject is None
                if task_final.content_material:
                    nm = task_final.content_material
                    nm.markdown_content = final_markdown
                    nm.save()
                else:
                    nm = ContentMaterial.objects.create(title=final_course_title, short_description=task_final.structured_content["metadata"].get("descripcion_corta", ""), markdown_content=final_markdown, master_category=master_category, sub_category=sub_category, creator=task_final.assigned_to, is_free_content=is_free, is_public=True)
                if not is_free and task_final.subject:
                     fam = task_final.subject.content_hash_family
                     if fam: 
                         fam.content_material = nm
                         fam.save()
                         nm.subject.add(*fam.subjects.all())
                     else:
                         nm.subject.add(task_final.subject)
                task_final.content_material = nm
                task_final.status = PendingContentTask.StatusChoices.COMPLETED
                task_final.save(update_fields=["status", "content_material"])
            _send_completion_notifications(nm)
            log_task_event(task_id, "TAREA COMPLETADA EXITOSAMENTE.")

    except Exception as e:
        err_str = str(e)
        is_transient = isinstance(e, (TimeoutError, ConnectionError, OSError, OperationalError, InterfaceError)) or "Resource" in err_str or "429" in err_str or "Quota" in err_str
        
        if is_transient:
             log_task_event(task_id, f"Error Transitorio Global (Escape): {err_str}. Reintentando...", is_error=True)
             raise self.retry(exc=e, countdown=300)
        else:
             log_task_event(task_id, f"ERROR FATAL DE CÓDIGO: {err_str}", is_error=True)
             if task:
                 task.status = PendingContentTask.StatusChoices.FAILED_FATAL
                 task.last_error = traceback.format_exc()
                 task.save(update_fields=["status", "last_error"])

    finally:
        db.close_old_connections()

# --- [UPDATED TASK V3: REAL CONTEXT SUPPORT] ---
# Esta tarea soporta la inyección de contexto real del temario
@shared_task(bind=True, max_retries=3)
def generate_exam_task(self, exam_uuid, context_text=None, topic=None):
    """
    Orquesta la generación del examen usando CONTEXTO REAL (Rango de Temario).
    """
    try:
        from assessment_v2.models.main import Exam
        from assessment_v2.services.engine.factory import ExamFactory
        from assessment_v2.services.tracking import TrackingService
        from core.services.gemini_service import GeminiService
        import json
        
        logger.info(f"Starting generation for Exam {exam_uuid}. Topic: {topic}")
        exam = Exam.objects.get(uuid=exam_uuid)
        
        exam.status = Exam.STATUS_GENERATING
        exam.save()

        strategy = ExamFactory.get_strategy(
            exam.archetype_id,
            exam.sub_archetype_id,
            exam.itinerary_id,
            exam.pedagogical_level
        )

        system_prompt = strategy.get_system_prompt()
        base_structure = strategy.generate_structure()
        
        # INYECCIÓN DEL MATERIAL DE ESTUDIO (RANGO SELECCIONADO)
        material_prompt = ""
        if context_text:
            # Truncamos si es excesivo para evitar error 429/ContextLimit
            safe_context = context_text[:50000] 
            material_prompt = f"\\n\\nMATERIAL DE REFERENCIA (FUENTE DE VERDAD):\\n{safe_context}\\n\\n"

        user_message = (
            f"CONTEXTO ACADÉMICO: {topic or 'General'}. "
            f"{material_prompt}"
            f"INSTRUCCIÓN: Genera el examen basándote EXCLUSIVAMENTE en el Material de Referencia proporcionado. "
            f"Rellena el siguiente esquema JSON: {json.dumps(base_structure)}"
        )

        # Ejecución con captura de metadatos de tokens (V06DOC_STRUCTURE)
        ai_response, usage_metadata = GeminiService.generate(
            system_prompt=system_prompt,
            user_prompt=user_message,
            temperature=0.5
        )

        if isinstance(ai_response, str):
            cleaned_response = ai_response.replace('```json', '').replace('```', '').strip()
            exam_structure = json.loads(cleaned_response)
        else:
            exam_structure = ai_response

        if 'subdivision_sequence' not in exam_structure:
            raise ValueError("Estructura inválida recibida de IA.")

                # Registro de consumo y costes
        if usage_metadata:
            TrackingService.record_usage(
                user=exam.user,
                exam=exam,
                model_name="gemini-2.5-flash-lite",
                input_tokens=usage_metadata.get('prompt_token_count', 0),
                output_tokens=usage_metadata.get('candidates_token_count', 0)
            )

        exam.structure = exam_structure
        exam.status = Exam.STATUS_READY
        exam.save()
        logger.info(f"Exam {exam_uuid} generated successfully.")

    except Exception as e:
        logger.error(f"Error generating exam {exam_uuid}: {str(e)}")
        if 'exam' in locals():
            exam.status = Exam.STATUS_ERROR
            exam.error_log = str(e)
            exam.save()
        raise self.retry(exc=e, countdown=60)
