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

def log_task_event(task_id: str, message: str, is_error: bool = False, payload: dict = None):
    try:
        entry = {"timestamp": datetime.utcnow().isoformat() + "Z", "level": "ERROR" if is_error else "INFO", "message": message}
        if payload: entry["payload"] = str(payload)[:2000]
        with transaction.atomic():
            task = PendingContentTask.objects.select_for_update().get(id=task_id)
            if task.task_log is None: task.task_log = []
            task.task_log.append(entry)
            task.save(update_fields=['task_log'])
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
    yaml = ["---", f'titulo: "{course_title}"', f"categoria_general: \"{classification.get('categoria_general', 'Desconocida')}\"", "---"]
    intro = [f"# {course_title}", metadata.get('descripcion_corta', ''), "## Tabla de Contenidos"]
    body = []
    parsed = _parse_master_schema(master_schema)
    chunk_map = {slugify(parsed[c.order - 1][1]): c for c in chunks}
    for level, title in parsed:
        slug = slugify(title)
        c = chunk_map.get(slug)
        body.append(f'<a id="{slug}"></a>\n{"#" * level} {title}\n{c.content if c else "Error."}')
    return "\n\n".join(yaml + intro + body)

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
        
        send_mail(
            subject=subject,
            message=body_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[exam.user.email],
            fail_silently=True
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

@shared_task(bind=True)
def global_orchestrator_task(self):
    try:
        _purge_zombie_tasks()
        _process_quarantine_requests()
        _check_and_perform_daily_reset()
        db.close_old_connections()
        automation_settings = AutomationSettings.load()
        if not automation_settings.is_running: return
        
        active_key = automation_settings.active_api_key
        if not active_key or not active_key.is_enabled or active_key.is_quarantined:
            next_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
            if next_key:
                automation_settings.active_api_key = next_key
                automation_settings.save(update_fields=['active_api_key'])
            else: return
    except Exception as e:
        logger.critical(f"Error orquestador: {e}")

@shared_task(bind=True, time_limit=21600)
def generate_full_course_task(self, task_id):
    """Restored logic V24.13 ULTRA-BLINDADO."""
    db.close_old_connections()
    logger.info(f"[V24.13 ULTRA-BLINDADO] Iniciando Tarea {task_id}.")
    task = None
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
                 raise self.retry(countdown=900)

        task = PendingContentTask.objects.select_related('subject__academic_year__degree__branch__university', 'subject__content_hash_family').get(id=task_id)
        if task.status == PendingContentTask.StatusChoices.FAILED_FATAL: return

        PendingContentTask.objects.filter(id=task_id).update(global_actuation_count=F('global_actuation_count') + 1)
        task.refresh_from_db(fields=['global_actuation_count'])
        
        if task.global_actuation_count > automation_settings.max_task_actuations:
            task.status = PendingContentTask.StatusChoices.FAILED_FATAL
            task.save(update_fields=["status"])
            return

        if task.status in [PendingContentTask.StatusChoices.PENDING, PendingContentTask.StatusChoices.FAILED_RETRYABLE, PendingContentTask.StatusChoices.FAILED_QUOTA]:
            task.status = PendingContentTask.StatusChoices.PROCESSING
            task.save(update_fields=["status"])

        if not task.structured_content or "master_schema" not in task.structured_content:
            log_task_event(task_id, "Generando Plan de Trabajo...")
            topic_description = task.subject.name if task.subject else task.prompt_text
            metadata_prompt = generate_course_metadata_prompt(topic_description, "") + "\n\nJSON Only."
            success, response_text, _, usage = _safe_generate_content(metadata_prompt, logger_callback=lambda m, level="INFO": log_task_event(task_id, m))
            if not success: raise self.retry(countdown=60)
            
            metadata = json.loads(clean_json_response(response_text))
            schema_prompt = generate_master_schema_prompt(topic_description, "", "", "")
            success, schema_text, _, _ = _safe_generate_content(schema_prompt, logger_callback=lambda m, level="INFO": log_task_event(task_id, m))
            if not success: raise self.retry(countdown=60)
            
            task.section_count = len(_parse_master_schema(schema_text))
            task.structured_content = {"metadata": metadata, "master_schema": schema_text, "academic_context": ""}
            task.save(update_fields=["structured_content", "section_count"])

        parsed_schema = _parse_master_schema(task.structured_content["master_schema"])
        for index, (_, title) in enumerate(parsed_schema, 1):
            if GeneratedContentChunk.objects.filter(task=task, order=index).exists(): continue
            prompt = generate_atomic_content_prompt(task.subject.name if task.subject else task.course_title, title, task.structured_content["master_schema"], "")
            success, content, _, _ = _safe_generate_content(prompt, logger_callback=lambda m, level="INFO": log_task_event(task_id, m))
            if success:
                c, s = _parse_markdown_with_separator(content)
                GeneratedContentChunk.objects.create(task=task, order=index, content=c, ai_sources=s)
                time.sleep(5)
            else: raise self.retry(countdown=70)

        task.refresh_from_db()
        if task.content_chunks.count() >= task.section_count:
            final_md = _assemble_final_markdown_from_chunks(task.subject.name if task.subject else task.course_title, task.structured_content["metadata"], task.structured_content["master_schema"], list(task.content_chunks.all()))
            with transaction.atomic():
                nm = ContentMaterial.objects.create(title=task.subject.name if task.subject else task.course_title, markdown_content=final_md, creator=task.assigned_to, is_public=True)
                if task.subject: nm.subject.add(task.subject)
                task.content_material = nm
                task.status = PendingContentTask.StatusChoices.COMPLETED
                task.save(update_fields=["status", "content_material"])
            _send_completion_notifications(nm)
    except Exception as e:
        if isinstance(e, Retry): raise e
        if task:
            task.status = PendingContentTask.StatusChoices.FAILED_FATAL
            task.last_error = traceback.format_exc()
            task.save(update_fields=["status", "last_error"])

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
            exam.event_log.append({"ts": timezone.now().isoformat(), "msg": "Iniciando Skeleton-First"})
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
            
            while not section_success and local_retries < MAX_LOCAL_RETRIES:
                success, resp, key_name, usage = _safe_generate_content(
                    u_prompt_augmented,
                    system_instruction=s_prompt,
                    response_schema=strategy.get_output_schema(),
                    logger_callback=lambda m, level="INFO": exam.event_log.append({"ts": timezone.now().isoformat(), "msg": m}) or exam.save(update_fields=['event_log'])
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
                        
                        for i_idx, i_data in enumerate(items):
                            if i_idx < len(db_items):
                                db_item = db_items[i_idx]
                                db_item.content = i_data.get('content', {})
                                db_item.grading_logic = i_data.get('grading_logic', {})
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
                        error_msg = f"Error Parseo JSON Sección {s_info['subdivision_id']} (Intento {local_retries}/{MAX_LOCAL_RETRIES}): {parse_err}"
                        exam.event_log.append({"ts": timezone.now().isoformat(), "msg": error_msg})
                        exam.save(update_fields=['event_log'])
                        time.sleep(15)
                else:
                    local_retries += 1
                    error_msg = f"Fallo IA Sección {s_info['subdivision_id']} (Intento {local_retries}/{MAX_LOCAL_RETRIES}): {resp}"
                    exam.event_log.append({"ts": timezone.now().isoformat(), "msg": error_msg})
                    exam.save(update_fields=['event_log'])
                    time.sleep(15)
            
            # Si tras los reintentos locales falla, abortamos fatalmente el examen
            if not section_success:
                fatal_msg = f"ABORTO FATAL: La Sección {s_info['subdivision_id']} no pudo generarse tras {MAX_LOCAL_RETRIES} intentos."
                exam.event_log.append({"ts": timezone.now().isoformat(), "msg": fatal_msg})
                exam.save(update_fields=['event_log'])
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
