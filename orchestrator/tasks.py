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
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
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
from core.services.gemini_service import generate_text_content, generate_audio_content, clean_json_response, AIServiceCriticalError

from core.services.prompt_generators import (
    generate_course_metadata_prompt,
    generate_master_schema_prompt,
    generate_atomic_content_prompt
)
from messaging.push_utils import send_notification_to_user
from core.utils import send_unified_notification

# --- NUEVAS IMPORTACIONES HITO 6 ---
from assessment_v2.models.main import Exam, ExamSection, ExamItem
from assessment_v2.services.engine.factory import ExamFactory
from assessment_v2.services.engine.logic import AcademicDeductor
from assessment_v2.services.tracking import TrackingService

logger = logging.getLogger(__name__)
User = get_user_model()

QUARANTINE_MAILBOX_FILE = os.path.join(settings.BASE_DIR, "quarantine_requests.log")

# ==============================================================================
# SECCIÓN 1: FUNCIONES AUXILIARES DEL ORQUESTADOR (PRESERVADAS)
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
        logger.error(f"Error en event_log: {e}")

def _send_admin_notification(title, body):
    try:
        admins = CustomUser.objects.filter(is_superuser=True, is_active=True)
        if not admins.exists(): return
        email_subject = f"[CampuStudiOnline Automation] {title}"
        recipient_list = [admin.email for admin in admins]
        context = {'title': title, 'message_body': body, 'dashboard_url': 'https://www.campustudionline.com/admin/'}
        html_message = render_to_string('orchestrator/email/admin_notification.html', context)
        send_mail(subject=email_subject, message=body, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=recipient_list, fail_silently=True, html_message=html_message)
    except Exception as e:
        logger.error(f"Error notificación admin: {e}")

def _process_quarantine_requests():
    if not os.path.exists(QUARANTINE_MAILBOX_FILE): return
    try:
        with open(QUARANTINE_MAILBOX_FILE, "r") as f:
            key_ids = set(line.strip() for line in f if line.strip().isdigit())
        if not key_ids:
            os.remove(QUARANTINE_MAILBOX_FILE)
            return
        with transaction.atomic():
            ApiKey.objects.filter(id__in=key_ids).update(is_quarantined=True)
        os.remove(QUARANTINE_MAILBOX_FILE)
    except Exception as e:
        logger.error(f"Error procesando buzón: {e}")


def _request_quarantine_via_mailbox(api_key):
    """Solicita cuarentena persistente escribiendo en el buzón (thread-safe)."""
    try:
        with open(QUARANTINE_MAILBOX_FILE, "a") as f:
            f.write(f"{api_key.id}\n")
    except Exception as e:
        logger.error(f"Error solicitando cuarentena: {e}")

def _check_and_perform_daily_reset():
    try:
        automation_settings = AutomationSettings.load()
        madrid_tz = pytz.timezone('Europe/Madrid')
        now_madrid = timezone.now().astimezone(madrid_tz)
        if automation_settings.last_quarantine_reset_date >= now_madrid.date(): return
        if now_madrid.time() >= automation_settings.quarantine_reset_time:
            ApiKey.objects.filter(is_quarantined=True).update(is_quarantined=False)
            automation_settings.last_quarantine_reset_date = now_madrid.date()
            automation_settings.save(update_fields=["last_quarantine_reset_date"])
    except Exception as e:
        logger.error(f"Error reset diario: {e}")

def _purge_zombie_tasks():
    try:
        automation_settings = AutomationSettings.load()
        threshold = timezone.now() - timedelta(hours=automation_settings.zombie_task_threshold_hours)
        PendingContentTask.objects.exclude(status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.COMPLETED]).filter(updated_at__lt=threshold).delete()
    except Exception as e:
        logger.error(f"Error purga zombies: {e}")


# [HITO 6] AUDIO GENERATION HELPER / FUNCIÓN AUXILIAR PARA GENERAR AUDIO
def _generate_item_audio(item_id, text, api_key):
    """
    Converts item text to speech and saves to media/assessment/audio/.
    ---
    Convierte el texto del ítem en voz y lo guarda en media/assessment/audio/.
    """
    try:
        success, audio_bytes, _ = generate_audio_content(text, api_key)
        if success and audio_bytes:
            filename = f"assessment/audio/item_{item_id}.mp3"
            if default_storage.exists(filename):
                default_storage.delete(filename)
            path = default_storage.save(filename, ContentFile(audio_bytes))
            return default_storage.url(path)
    except Exception as e:
        logger.error(f"Error generando audio para ítem {item_id}: {e}")
    return None
# ==============================================================================
# SECCIÓN 2: GENERACIÓN DE CONTENIDO (RESTAURADO V24.13)
# ==============================================================================


def _safe_generate_content(prompt, system_instruction=None, response_schema=None, logger_callback=None):
    """
    [HITO 37 RESTORED] Wrapper de Rotación en Caliente (Hot-Swap).
    Gestiona Errores 429/Cuota, Strikes y Rotación de Keys transparente.
    """
    while True:
        # 1. Sincronización
        automation_settings = AutomationSettings.load()
        api_key = automation_settings.active_api_key
        
        # 2. Validación de Clave Activa
        if not api_key or not api_key.is_enabled or api_key.is_quarantined:
                api_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
                if api_key:
                    automation_settings.active_api_key = api_key
                    automation_settings.save(update_fields=['active_api_key'])
                else:
                    if logger_callback: logger_callback("SIN CLAVES DISPONIBLES. Esperando 5m...", level="ERROR")
                    time.sleep(300)
                    continue

        if logger_callback: logger_callback(f"Llamando a API... (Clave: {api_key.name})")
        
        try:
            # Llamada original
            success, text, key_name, usage = generate_text_content(
                prompt, 
                system_instruction=system_instruction,
                api_key=api_key,
                response_schema=response_schema
            )
        except Exception as e:
            success = False
            text = str(e)
            usage = {}
        
        if success:
            # Limpiar strikes si hubo éxito
            if api_key.consecutive_failures > 0:
                api_key.consecutive_failures = 0
                api_key.save(update_fields=['consecutive_failures'])
            return True, text, api_key.name, usage
        
        else:
            # 3. Gestión de Errores Estándar
            error_str = str(text)
            is_quota = "429" in error_str or "Resource" in error_str or "Quota" in error_str
            
            if is_quota:
                api_key.refresh_from_db()
                api_key.consecutive_failures += 1
                api_key.save(update_fields=["consecutive_failures"])
                
                if api_key.consecutive_failures >= 4:
                    api_key.is_quarantined = True
                    api_key.save(update_fields=["is_quarantined"])
                    _request_quarantine_via_mailbox(api_key)
                    if logger_callback: logger_callback(f"ROTACIÓN FORZADA: Clave {api_key.name} a Cuarentena.")
                    
                    # Intentar rotar inmediatamente para el siguiente loop
                    next_k = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).exclude(id=api_key.id).first()
                    if next_k:
                        automation_settings.active_api_key = next_k
                        automation_settings.save(update_fields=['active_api_key'])
                else:
                    if logger_callback: logger_callback(f"STRIKE {api_key.consecutive_failures}/4 ({api_key.name}).", level="WARNING")
                continue 
            else:
                # Error no relacionado con cuota (ej: 500, overload), devolvemos el error.
                return False, text, api_key.name, {}

def deep_validate_json_structure(expected, received, path="root"):
    """
    Validación estricta recursiva del esqueleto JSON frente a la salida de la IA.
    Garantiza que la IA actúe solo como máquina de relleno, sin alterar estructura.
    """
    if isinstance(expected, dict):
        if not isinstance(received, dict):
            raise ValueError(f"[{path}] Se esperaba un objeto/diccionario, se recibió {type(received).__name__}")
        for k, v in expected.items():
            if k not in received:
                raise ValueError(f"[{path}] Falta la clave obligatoria: '{k}'")
            deep_validate_json_structure(v, received[k], f"{path}.{k}")
    elif isinstance(expected, list):
        if not isinstance(received, list):
            raise ValueError(f"[{path}] Se esperaba un array/lista, se recibió {type(received).__name__}")
        # No verificamos longitud de lista, la IA rellena los marcadores.

def log_task_event(task_id: str, message: str, is_error: bool = False, payload: dict = None):
    try:
        entry = {"timestamp": datetime.utcnow().isoformat() + "Z", "level": "ERROR" if is_error else "INFO", "message": message}
        if payload: entry["payload"] = str(payload)[:2000]
        with transaction.atomic():
            task = PendingContentTask.objects.select_for_update().get(id=task_id)
            if task.task_log is None: task.task_log = []
            task.task_log.append(entry)
            task.updated_at = timezone.now()
            task.save(update_fields=['task_log', 'updated_at'])
    except Exception as e:
        logger.error(f"Error log_task_event: {e}")

def _parse_master_schema(markdown_text: str) -> list:
    return [(len(hashes), title.strip()) for hashes, title in re.findall(r"^(##+)\s(.*)", markdown_text, re.MULTILINE)]

def _parse_markdown_with_separator(raw_text: str) -> tuple[str, str]:
    sep = r"(?i:^[-*_#]*\s*(?:FUENTES|BIBLIOGRAF[ÍI]A|REFERENCIAS)\s*[-*_#]*$)"
    parts = list(re.finditer(sep, raw_text, re.MULTILINE))
    if parts:
        return raw_text[:parts[-1].start()].strip(), raw_text[parts[-1].end():].strip()
    return raw_text.strip(), ""

def _assemble_final_markdown_from_chunks(course_title: str, metadata: dict, master_schema: str, chunks: list[GeneratedContentChunk]) -> str:
    classification = metadata.get("clasificacion_intelectual", {})
    yaml_header =["---", f'titulo: "{course_title}"', f'descripcion_corta: "{metadata.get("descripcion_corta", "")}"', f'categoria_general: "{classification.get("categoria_general", "Desconocida")}"', f'subcategoria: "{classification.get("subcategoria", "Desconocida")}"', f'palabras_clave: {json.dumps(classification.get("palabras_clave", []))}', "---"]
    parsed_schema = _parse_master_schema(master_schema)
    fuentes_title = "Fuentes y Bibliografía"
    fuentes_slug = slugify(fuentes_title)
    parsed_schema.append((2, fuentes_title))
    toc_entries =[]
    for level, title in parsed_schema:
        slug = slugify(title)
        indent = "    " * (level - 2)
        toc_entries.append(f"{indent}*[{title}](#{slug})")
    introduction =[f"# {course_title}", f"{metadata.get('descripcion_corta', 'Descripción no disponible.')}", '<a id="tabla-de-contenidos"></a>', "## Tabla de Contenidos", "\n".join(toc_entries)]
    content_body =[]
    original_parsed_schema = _parse_master_schema(master_schema)
    chunk_map = {slugify(original_parsed_schema[chunk.order - 1][1]): chunk for chunk in chunks}
    for level, title in original_parsed_schema:
        slug = slugify(title)
        chunk = chunk_map.get(slug)
        content_text = chunk.content if chunk else f"### Error\n\nEl contenido para la sección '{title}' no pudo ser localizado."
        heading_hashes = "#" * level
        content_body.append(f'<a id="{slug}"></a>')
        content_body.append(f"{heading_hashes} {title}")
        content_body.append(content_text)
        if level == 2:
            content_body.append("\n[⬆️ Volver al índice](#tabla-de-contenidos)")
    all_sources_text =[chunk.ai_sources for chunk in chunks if chunk.ai_sources]
    if all_sources_text:
        unique_references = set()
        for source_block in all_sources_text:
            for line in source_block.split('\n'):
                cleaned_line = line.strip()
                if cleaned_line:
                    unique_references.add(cleaned_line)
        sorted_references = sorted(list(unique_references))
        formatted_bibliography = "\n".join(f"- {ref}" for ref in sorted_references)
        bibliography_section =[f'<a id="{fuentes_slug}"></a>', f"## {fuentes_title}", formatted_bibliography, "\n[⬆️ Volver al índice](#tabla-de-contenidos)"]
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
        content_url = new_content.get_absolute_url()
        full_url = f"https://{settings.ALLOWED_HOSTS[0]}{content_url}"
        push_title = "¡Contenido Disponible!"
        push_body = f"El material de estudio para '{new_content.title}' ya está disponible."
        email_subject = f"[CampuStudiOnline] El contenido para '{new_content.title}' está listo"
        email_body_text = (f"¡Hola!\n\nNos complace informarte que el material de estudio para la asignatura '{new_content.title}' que solicitaste ha sido generado y ya está disponible en la plataforma.\n\n"
                           f"Puedes acceder a él directamente a través del siguiente enlace:\n{full_url}\n\n"
                           f"Gracias por tu paciencia y por ayudarnos a mejorar CampuStudiOnline.\n\n"
                           f"Atentamente,\nEl equipo de CampuStudiOnline")
        context = {'content_title': new_content.title, 'content_url': full_url}
        html_message = render_to_string('orchestrator/email/content_completion.html', context)
        for user in requesters:
            send_notification_to_user(user, push_title, push_body, url=content_url)
            send_mail(subject=email_subject, message=email_body_text, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user.email], fail_silently=True, html_message=html_message)
        content_request.status = ContentRequest.StatusChoices.FULFILLED
        content_request.save(update_fields=["status"])
    except Exception as e:
        logger.error(f"Error notifications: {e}")

def _send_exam_failure_notification(exam):
    """
    Notifies the user via Email and Push about a fatal generation error.
    Notifica al usuario vía Email y Push sobre un error fatal de generación.
    Ref: V06DOC_LOGIC_MAPPING Section 3 (Incidencia 27).
    """
    try:
        from django.utils.translation import gettext as _
        subject = _("[CampuStudiOnline] Error en la generación de tu evaluación")
        body_text = _(
            f"Hola,\n\nLamentamos informarte que el servicio de generación de exámenes no está disponible temporalmente "
            f"para la asignatura '{exam.content_copy.original_content.title}'.\n\n"
            "Por favor, inténtalo de nuevo más tarde. No se ha realizado ningún cargo en tu cuota semanal.\n\n"
            "Disculpa las molestias.\nEl equipo de CampuStudiOnline"
        )
        
        context = {
            'course_title': exam.content_copy.original_content.title,
            'dashboard_url': f"https://{settings.ALLOWED_HOSTS[0]}/"
        }
        html_message = render_to_string('orchestrator/email/exam_failure.html', context)

        send_mail(
            subject=subject,
            message=body_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[exam.user.email],
            fail_silently=True,
            html_message=html_message
        )
        
        send_unified_notification(
            exam.user, 
            _("Servicio no disponible"), 
            _("No se pudo generar el examen. Por favor, inténtelo de nuevo más tarde."), 
            reverse('assessment_v2:dashboard')
        )
    except Exception as e:
        logger.error(f"Error en _send_exam_failure_notification: {e}")


def _get_next_subject_queryset(settings_obj):
    base_queryset = Subject.objects.filter(content_materials__isnull=True)
    active_task_subject_names = PendingContentTask.objects.exclude(status__in=[PendingContentTask.StatusChoices.COMPLETED, PendingContentTask.StatusChoices.FAILED_FATAL]).values_list('subject__name', flat=True).distinct()
    query = base_queryset.exclude(name__in=active_task_subject_names)
    if settings_obj.seed_branch: query = query.filter(academic_year__degree__branch=settings_obj.seed_branch)
    if settings_obj.seed_degree: query = query.filter(academic_year__degree=settings_obj.seed_degree)
    return query

# ==============================================================================
# SECCIÓN 3: TAREAS CELERY - CONTENIDO (PRESERVADA)
# ==============================================================================

def _advance_seed_filters_if_needed(automation_settings):
    if not any([automation_settings.seed_branch, automation_settings.seed_degree, automation_settings.seed_year]):
        return False
    from academic_structure.models import Subject
    from .models import PendingContentTask
    base_queryset = Subject.objects.filter(content_materials__isnull=True)
    active_task_subject_names = PendingContentTask.objects.exclude(status__in=[PendingContentTask.StatusChoices.COMPLETED, PendingContentTask.StatusChoices.FAILED_FATAL]).values_list('subject__name', flat=True).distinct()
    query = base_queryset.exclude(name__in=active_task_subject_names)
    if automation_settings.seed_branch: query = query.filter(academic_year__degree__branch=automation_settings.seed_branch)
    if automation_settings.seed_degree: query = query.filter(academic_year__degree=automation_settings.seed_degree)
    
    if not query.exists():
        if automation_settings.seed_year:
            automation_settings.seed_year = ""
            automation_settings.save(update_fields=['seed_year'])
            return True
        if automation_settings.seed_degree:
            automation_settings.seed_degree = None
            automation_settings.save(update_fields=['seed_degree'])
            return True
        if automation_settings.seed_branch:
            automation_settings.seed_branch = None
            automation_settings.save(update_fields=['seed_branch'])
            return True
    return False

@shared_task(bind=True)
def global_orchestrator_task(self):
    try:
        db.close_old_connections()
        # [HOTFIX] DEBOUNCE: Evitar ejecuciones superpuestas
        try:
            settings_check = AutomationSettings.load()
            if settings_check.last_run_timestamp:
                delta = timezone.now() - settings_check.last_run_timestamp
                if delta.total_seconds() < 45:
                    logger.warning(f'ORCHESTRATOR DEBOUNCE: Ejecución omitida (Delta: {delta.total_seconds():.1f}s < 45s).')
                    return
        except Exception:
            pass

        _purge_zombie_tasks()
        _process_quarantine_requests()
        _check_and_perform_daily_reset()
        
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
            _log_structured_event("SINCRO: Clave activa no es válida. Buscando reemplazo.", "INFO")
            next_available_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
            if next_available_key:
                automation_settings.active_api_key = next_available_key
                automation_settings.save(update_fields=['active_api_key'])
                _log_structured_event(f"SINCRO EXITOSA: Nueva clave activa es '{next_available_key.name}'.", "INFO")
            else:
                status_msg = "HIBERNANDO (POOL AGOTADO): No hay claves disponibles."
                if automation_settings.last_run_status != status_msg:
                    _log_structured_event(status_msg, "WARNING")
                    automation_settings.last_run_status = status_msg
                    automation_settings.save(update_fields=['last_run_status'])
                return
        
        automation_settings.refresh_from_db()

        # Rescate de Tareas de Contenido Zombies/Fallidas
        zombie_threshold = timezone.now() - timedelta(minutes=5)
        zombie_content_tasks = PendingContentTask.objects.filter(
            status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.PENDING], 
            updated_at__lt=zombie_threshold
        )
        for task in zombie_content_tasks:
            _log_structured_event(f"VIGILANTE: Tarea '{task.id}' ZOMBIE rescatada.", "WARNING")
            task.status = PendingContentTask.StatusChoices.FAILED_RETRYABLE
            task.save(update_fields=["status"])
            
        task_to_rescue = PendingContentTask.objects.filter(
            status__in=[PendingContentTask.StatusChoices.FAILED_RETRYABLE, PendingContentTask.StatusChoices.FAILED_QUOTA]
        ).order_by('created_at').first()
        
        if task_to_rescue:
            _log_structured_event(f"RESCATE: Re-encolando la tarea de contenido {task_to_rescue.id}.", "INFO")
            sc = task_to_rescue.structured_content or {}
            if sc.get("consecutive_quota_errors", 0) > 0:
                sc["consecutive_quota_errors"] = 0
                task_to_rescue.structured_content = sc
            task_to_rescue.status = PendingContentTask.StatusChoices.PENDING
            task_to_rescue.save(update_fields=["status", "structured_content"])
            generate_full_course_task.delay(str(task_to_rescue.id))
            
            automation_settings.last_run_status = f"AUTO-RECUPERACIÓN: Tarea re-encolada."
            automation_settings.last_run_timestamp = timezone.now()
            automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
            return

                # PRIORIDAD 0: Evaluaciones/Exámenes (HITO 6 - MÁXIMA PRIORIDAD)
        pending_exam = Exam.objects.filter(status='PENDING').order_by('created_at').first()
        if pending_exam:
            _log_structured_event(f"PRIORIDAD 0 (EXAM): Procesando examen {pending_exam.uuid}.", "INFO")
            
            # Marcamos actividad para evitar condiciones de carrera
            pending_exam.updated_at = timezone.now()
            pending_exam.save(update_fields=['updated_at'])
            
            generate_exam_task.delay(str(pending_exam.uuid))
            
            status_msg = f"TAREA LANZADA (EXAM): '{pending_exam.uuid}'."
            automation_settings.last_run_status = status_msg
            automation_settings.last_run_timestamp = timezone.now()
            automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
            return

        # PRIORIDAD 1: Solicitudes de Usuarios (ContentRequest)
        approved_request = ContentRequest.objects.filter(status=ContentRequest.StatusChoices.APPROVED).order_by('created_at').first()
        if approved_request and approved_request.subject.content_materials.count() == 0:
            subject_to_process = approved_request.subject
            with transaction.atomic():
                req = ContentRequest.objects.select_for_update().get(id=approved_request.id)
                req.status = ContentRequest.StatusChoices.IN_PROGRESS
                req.save(update_fields=["status"])
            
            admin_user = CustomUser.objects.filter(is_superuser=True, is_active=True).order_by('pk').first()
            new_task = PendingContentTask.objects.create(
                subject=subject_to_process, 
                assigned_to=admin_user, 
                task_origin=PendingContentTask.TaskOrigin.APPROVED_REQUEST
            )
            generate_full_course_task.delay(str(new_task.id))
            
            status_msg = f"TAREA LANZADA (REQUEST): '{subject_to_process.name}'."
            _log_structured_event(status_msg, "INFO")
            automation_settings.last_run_status = status_msg
            automation_settings.last_run_timestamp = timezone.now()
            automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
            return

        if PendingContentTask.objects.filter(status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.PENDING]).exists():
            status_msg = "EN ESPERA: Hay tareas de contenido activas."
            if automation_settings.last_run_status != status_msg:
                automation_settings.last_run_status = status_msg
                automation_settings.save(update_fields=['last_run_status'])
            return

        # CONTROL DE GENERACIÓN MASIVA
        if not automation_settings.is_mass_generation_enabled:
            status_msg = "AHORRO DE ENERGÍA: Generación masiva desactivada. A la espera de solicitudes manuales."
            if automation_settings.last_run_status != status_msg:
                _log_structured_event(status_msg, "INFO")
                automation_settings.last_run_status = status_msg
                automation_settings.save(update_fields=['last_run_status'])
            return

        # PRIORIDAD 2: Generación Masiva (Mass Generation)
        while True:
            subject_qs = _get_next_subject_queryset(automation_settings)
            subject_to_process = subject_qs.order_by('?').first()
            if subject_to_process:
                admin_user = CustomUser.objects.filter(is_superuser=True, is_active=True).order_by('pk').first()
                new_task = PendingContentTask.objects.create(
                    subject=subject_to_process, 
                    assigned_to=admin_user, 
                    task_origin=PendingContentTask.TaskOrigin.MASS_GENERATION
                )
                generate_full_course_task.delay(str(new_task.id))
                
                status_msg = f"TAREA LANZADA (MASS-GEN): '{subject_to_process.name}'."
                _log_structured_event(status_msg, "INFO")
                automation_settings.last_run_status = status_msg
                automation_settings.last_run_timestamp = timezone.now()
                automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
                break
            else:
                if _advance_seed_filters_if_needed(automation_settings):
                    continue
                else:
                    final_message = "SIN TRABAJO: No quedan más asignaturas para procesar."
                    if automation_settings.last_run_status != final_message:
                        _log_structured_event(final_message, "INFO")
                        automation_settings.last_run_status = final_message
                        automation_settings.save(update_fields=['last_run_status'])
                    break

    except Exception as e:
        logger.critical(f"Error orquestador: {e}", exc_info=True)


@shared_task(bind=True, time_limit=21600, acks_late=True, rate_limit='12/m')
def generate_full_course_task(self, task_id):
    db.close_old_connections()
    logger.info(f"[V24.14 503-AWARE] Iniciando Tarea {task_id}.")
    task = None
    api_key = None
    try:
        # --- BLOQUE DE INICIALIZACIÓN Y FUSIBLE ---
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

        if task.status in[PendingContentTask.StatusChoices.PENDING, PendingContentTask.StatusChoices.FAILED_RETRYABLE, PendingContentTask.StatusChoices.FAILED_QUOTA]:
            task.status = PendingContentTask.StatusChoices.PROCESSING
            task.save(update_fields=["status"])
            log_task_event(task_id, "Tarea iniciada (Status -> PROCESSING).")

        # --- FASE 1: GENERACIÓN DE PLAN ---
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
                    academic_context = f"- Universidad: {degree.branch.university.name}\n- Rama: {degree.branch.name}\n- Titulación: {degree.name}"
                    learning_objectives = json.dumps(task.subject.learning_objectives, ensure_ascii=False) if task.subject.learning_objectives else ""
                    syllabus = json.dumps(task.subject.course_content_outline, ensure_ascii=False) if task.subject.course_content_outline else ""
                else:
                    topic_description = task.prompt_text
                    academic_context = ""
                    learning_objectives = ""
                    syllabus = ""
                    
                metadata_prompt = generate_course_metadata_prompt(topic_description, academic_context) + "\n\nJSON Only."
                
                try:
                    success, response_text, _, _ = generate_text_content(metadata_prompt, api_key=api_key, task_id=task_id)
                except Exception as ex:
                    success = False
                    response_text = str(ex)

                if not success:
                    error_str = str(response_text)
                    is_quota = "429" in error_str or "Resource" in error_str or "Quota" in error_str
                    is_server_overload = "503" in error_str or "UNAVAILABLE" in error_str or "Overloaded" in error_str
                    
                    if is_server_overload:
                        log_task_event(task_id, f"GOOGLE OVERLOAD (503). Esperando 45s antes de reintentar con {api_key.name}...", is_error=True)
                        time.sleep(45)
                        # NO rotamos, NO sumamos strike. Simplemente reintentamos el bucle.
                        continue

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
                    success, schema_or_error, _, _ = generate_text_content(schema_prompt, api_key=api_key, task_id=task_id)
                except Exception as ex:
                    success = False
                    schema_or_error = str(ex)
                
                if not success:
                    error_str = str(schema_or_error)
                    is_quota = "429" in error_str or "Resource" in error_str or "Quota" in error_str
                    is_server_overload = "503" in error_str or "UNAVAILABLE" in error_str or "Overloaded" in error_str

                    if is_server_overload:
                        log_task_event(task_id, f"GOOGLE OVERLOAD (503) en ESQUEMA. Esperando 45s...", is_error=True)
                        time.sleep(45)
                        continue

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
                if task.structured_content and task.structured_content.get('manual_classification'):
                    new_structured_content['manual_classification'] = task.structured_content['manual_classification']
                    
                task.section_count = section_count
                task.structured_content = new_structured_content
                task.save(update_fields=["structured_content", "section_count"])
                log_task_event(task_id, f"Plan generado: {section_count} secciones.")
                break 

        # --- FASE 2: GENERACIÓN DE CHUNKS ---
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
                    success, content_or_error, _, _ = generate_text_content(initial_prompt, api_key=api_key, task_id=task_id)
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
                    is_quota = "429" in error_str or "Resource" in error_str or "Quota" in error_str
                    is_server_overload = "503" in error_str or "UNAVAILABLE" in error_str or "Overloaded" in error_str

                    if is_server_overload:
                        log_task_event(task_id, f"GOOGLE OVERLOAD (503). Esperando 45s antes de reintentar con {api_key.name}...", is_error=True)
                        time.sleep(45)
                        # NO rotamos, NO sumamos strike.
                        continue

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

        # --- FINALIZACIÓN ---
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

# ==============================================================================
# HITO 6: GENERACIÓN DE EXAMEN (SKELETON-FIRST ATÓMICO)
# ==============================================================================

@shared_task(bind=True, time_limit=1800, max_retries=3)
def generate_exam_task(self, exam_uuid, context_text=None, topic=None):
    db.close_old_connections()
    exam = None
    try:
        exam = Exam.objects.select_related('user', 'content_copy').get(uuid=exam_uuid)
        if self.request.retries == 0:
            exam.status = 'GENERATING'
            exam.event_log.append({"ts": timezone.now().isoformat(), "msg": f"Iniciando Skeleton-First (Examen: {str(exam.uuid)[:8]})"})
            exam.save(update_fields=['status', 'event_log'])

        material = exam.content_copy.original_content
        subject = material.subject.first()
        
        # PROTOCOLO DE RESILIENCIA (10 MIN RETRY)
        try:
            metadata = AcademicDeductor.get_context_metadata(subject, context_title=material.title)
        except AIServiceCriticalError as e:
            exam.event_log.append({"ts": timezone.now().isoformat(), "msg": "API Clasificación Fallida. Reintento 10min."})
            exam.save(update_fields=['event_log'])
            raise self.retry(exc=e, countdown=600)
        
        exam.archetype_id = metadata['archetype_id']
        exam.sub_archetype_id = metadata['sub_archetype_id']
        exam.itinerary_id = metadata['itinerary_id']
        exam.pedagogical_level = metadata['pedagogical_level']
        # [Strategy Delegation] Immersion mode logic moved to strategy
        exam.target_language_code = metadata.get('target_language_code', 'es')
        exam.localized_sections = metadata.get('localized_sections', {})
        
        strategy = ExamFactory.get_strategy(
            archetype_id=exam.archetype_id,
            sub_archetype_id=exam.sub_archetype_id,
            pedagogical_level=exam.pedagogical_level,
            itinerary_id=exam.itinerary_id,
            target_language_code=exam.target_language_code,
            localized_sections=exam.localized_sections
        )
        exam.immersion_mode = strategy.get_immersion_mode()
        exam.grading_params = strategy._get_grading_params()
        # [HITO 6 FIX] Discrepancia 1: Secuencialidad obligatoria para Lenguas
        if exam.archetype_id == 'ARCH_LANG':
            exam.is_sequential = True
        exam.save()

        # FASE ESTRUCTURAL (Skeleton-First Fijo)
        skeleton = strategy.get_exam_skeleton()
        with transaction.atomic():
            exam.sections.all().delete()
            sections_map = {}
            for idx, s_data in enumerate(skeleton):
                section = ExamSection.objects.create(
                    exam=exam, 
                    subdivision_id=s_data['subdivision_id'], 
                    title=s_data['title'],
                    instructions=s_data.get('instructions', ''), 
                    time_limit=s_data.get('time_limit', 0),
                    layout_mode=s_data.get('layout_mode', 'STANDARD'),
                    order=idx
                )
                sections_map[s_data['subdivision_id']] = section
                
                # Crear ítems vacíos con el esqueleto predefinido
                for i_idx, i_data in enumerate(s_data.get('items', [])):
                    ExamItem.objects.create(
                        section=section,
                        block_type=i_data.get('block_type', 'UNKNOWN'),
                        widget_id=i_data.get('widget_id', 'UNKNOWN'),
                        # [HITO 6] FIX: Inyección de parámetros técnicos de la Estrategia
                        level_requisite=i_data.get('level_requisite', 'MANDATORY'),
                        weight=i_data.get('weight', 1.00),
                        estimated_time=i_data.get('estimated_time', 0),
                        fail_logic=i_data.get('fail_logic', 'PENALTY'),
                        content={},
                        grading_logic={},
                        # [HITO 6] SKELETON-PROMPT BINDING: Persistir la instrucción de llenado
                        metadata={'task_instruction': i_data.get('task_instruction', '')},
                        order=i_idx
                    )
        
        # FASE DE LLENADO ATÓMICO (Bucle Iterativo por Sección)
        generated_titles = []
        usage_total = {"in": 0, "out": 0}
        
        for s_info in skeleton:
            db_sec = sections_map.get(s_info['subdivision_id'])
            if not db_sec: continue
            
            # Inyección de immersion_mode y pedagogical_level ELIMINADA (Bugfix: TypeError)
            s_prompt = strategy.get_system_prompt()
            
            u_prompt = strategy.get_user_prompt(
                context_text=context_text, topic=topic or subject.name,
                subdivision_id=s_info['subdivision_id'], generated_item_titles=generated_titles
            )
            
            db_items = list(db_sec.items.all().order_by('order'))
            if not db_items: continue
            
            # [HITO 6 BLINDAJE] Resiliencia Celery: Si el primer item ya tiene contenido, la sección está lista
            if db_items[0].content:
                for item in db_items:
                    generated_titles.append(str(item.content.get('stem', ''))[:30])
                continue
            
            # [HITO 6] SKELETON-PROMPT BINDING: Inyectar la instrucción específica por ítem
            widgets_info_list = []
            for i, item in enumerate(db_items):
                instruction = item.metadata.get('task_instruction', 'Generar contenido académico estándar para este widget.')
                widgets_info_list.append(f"Item {item.uuid} [{item.widget_id}]: {instruction}")
            
            widgets_info = "\n".join(widgets_info_list)
            u_prompt_augmented = f"{u_prompt}\n\nINSTRUCCIONES DE LLENADO POR ÍTEM (OBLIGATORIO):\n{widgets_info}"

            # [HITO 6 BLINDAJE] Bucle de reintentos local (Atómico) para evitar consumir max_retries de Celery
            section_success = False
            local_retries = 0
            MAX_LOCAL_RETRIES = 3
            
            # [FIX LOGGING] Crear un callback de logging con contexto
            def contextual_logger(message, level="INFO"):
                context_msg = f"{message} (Examen: {str(exam.uuid)[:8]}, Sección: {s_info['subdivision_id']})"
                exam.event_log.append({"ts": timezone.now().isoformat(), "msg": context_msg, "level": level})
                exam.save(update_fields=['event_log'])

            while not section_success and local_retries < MAX_LOCAL_RETRIES:
                success, resp, key_name, usage = _safe_generate_content(
                    u_prompt_augmented,
                    system_instruction=s_prompt,
                    response_schema=strategy.get_output_schema(),
                    logger_callback=contextual_logger
                )
                
                if success:
                    try:
                        usage_total["in"] += usage.get("input_tokens", 0)
                        usage_total["out"] += usage.get("output_tokens", 0)
                        parsed_resp = dirtyjson.loads(clean_json_response(resp))
                        items = parsed_resp.get("items", [])
                        
                        if "section_stimulus" in parsed_resp:
                            db_sec.section_stimulus = parsed_resp.get("section_stimulus", "")
                            db_sec.save(update_fields=["section_stimulus"])
                        
                        # [FIX] SKELETON-PROMPT BINDING: Mapeo estricto por UUID devuelto por la IA
                        db_items_map = {str(item.uuid): item for item in db_items}
                        for i_data in items:
                            ai_item_id = i_data.get('item_id')
                            db_item = db_items_map.get(str(ai_item_id))
                            
                            if db_item:
                                # [HITO 6 BLINDAJE] VALIDACIÓN ESTRICTA TRY-AND-FAIL (Deep Structure)
                                ai_content = i_data.get('content', {})
                                ai_grading = i_data.get('grading_logic', {})
                                
                                if db_item.content:
                                    deep_validate_json_structure(db_item.content, ai_content, "content")
                                if db_item.grading_logic:
                                    deep_validate_json_structure(db_item.grading_logic, ai_grading, "grading_logic")

                                db_item.content = ai_content
                                db_item.grading_logic = ai_grading
                                # [HITO 6 BLINDAJE] Preservar metadata original (TaskInstruction)
                                ai_metadata = i_data.get('metadata', {})
                                if 'task_instruction' in db_item.metadata:
                                    ai_metadata['task_instruction'] = db_item.metadata['task_instruction']
                                db_item.metadata = ai_metadata
                                # [HITO 6] AUDIO GENERATION TRIGGER (SD_LIST) / DISPARADOR DE AUDIO
                                if s_info['subdivision_id'] == 'SD_LIST':
                                    audio_text = db_sec.section_stimulus if db_sec.section_stimulus else db_item.content.get('stem', '')
                                    audio_url = _generate_item_audio(db_item.id, audio_text, automation_settings.active_api_key)
                                    if audio_url: db_item.content['media_assets'] = [audio_url]
                                db_item.save(update_fields=["content", "grading_logic", "metadata"])
                                generated_titles.append(str(i_data.get('content', {}).get('stem', ''))[:30])
                        
                        section_success = True
                        time.sleep(5)
                    except Exception as parse_err:
                        local_retries += 1
                        error_msg = f"Error Parseo JSON (Intento {local_retries}/{MAX_LOCAL_RETRIES}): {parse_err}"
                        contextual_logger(error_msg, level="ERROR")
                        time.sleep(15)
                else:
                    local_retries += 1
                    error_msg = f"Fallo IA (Intento {local_retries}/{MAX_LOCAL_RETRIES}): {resp}"
                    contextual_logger(error_msg, level="ERROR")
                    time.sleep(15)
            
            # Si tras los reintentos locales falla, abortamos fatalmente el examen
            if not section_success:
                fatal_msg = f"ABORTO FATAL: La Sección no pudo generarse tras {MAX_LOCAL_RETRIES} intentos."
                contextual_logger(fatal_msg, level="CRITICAL")
                raise AIServiceCriticalError(fatal_msg)

        TrackingService.record_usage(exam.user, exam, "gemini-2.5-flash-lite", usage_total["in"], usage_total["out"], "Restored-Key")
        exam.status = 'READY'
        exam.expiration_date = timezone.now() + timedelta(hours=24)
        exam.event_log.append({"ts": timezone.now().isoformat(), "msg": "Generación Completada. Caduca en 24h."})
        exam.save()

    except MaxRetriesExceededError:
        if exam:
            exam.status = 'ERROR'
            exam.error_log = "MaxRetriesExceeded: La IA falló repetidamente."
            exam.save(update_fields=['status', 'error_log'])
            
            # Notificación al Administrador (OBLIGATORIO)
            try:
                _send_admin_notification(f"FALLO CRÍTICO EXAMEN {exam.uuid}", f"El examen ha fallado tras agotar los reintentos de IA. Usuario: {exam.user.email}")
            except: pass

            # Notificación al Usuario (Incidencia 27)
            _send_exam_failure_notification(exam)
    except Exception as e:
        if isinstance(e, Retry): raise e
        if exam:
            exam.status = 'ERROR'
            exam.error_log = traceback.format_exc()
            exam.save()
            # Notificación al Usuario (Incidencia 27)
            _send_exam_failure_notification(exam)

