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

# ==============================================================================
# SECCIÓN 2: GENERACIÓN DE CONTENIDO (RESTAURADO V24.13)
# ==============================================================================

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
            success, response_text, _, usage = generate_text_content(metadata_prompt, api_key=api_key)
            if not success: raise self.retry(countdown=60)
            
            metadata = json.loads(clean_json_response(response_text))
            schema_prompt = generate_master_schema_prompt(topic_description, "", "", "")
            success, schema_text, _, _ = generate_text_content(schema_prompt, api_key=api_key)
            if not success: raise self.retry(countdown=60)
            
            task.section_count = len(_parse_master_schema(schema_text))
            task.structured_content = {"metadata": metadata, "master_schema": schema_text, "academic_context": ""}
            task.save(update_fields=["structured_content", "section_count"])

        parsed_schema = _parse_master_schema(task.structured_content["master_schema"])
        for index, (_, title) in enumerate(parsed_schema, 1):
            if GeneratedContentChunk.objects.filter(task=task, order=index).exists(): continue
            prompt = generate_atomic_content_prompt(task.subject.name if task.subject else task.course_title, title, task.structured_content["master_schema"], "")
            success, content, _, _ = generate_text_content(prompt, api_key=api_key)
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
        exam.immersion_mode = metadata['immersion_mode']
        
        strategy = ExamFactory.get_strategy(exam.archetype_id, exam.pedagogical_level, exam.itinerary_id)
        exam.grading_params = strategy._get_grading_params()
        exam.save()

        # FASE ESTRUCTURAL (Skeleton-First)
        section_plan = strategy.get_section_plan()
        with transaction.atomic():
            exam.sections.all().delete()
            sections_map = {}
            for idx, s_data in enumerate(section_plan):
                section = ExamSection.objects.create(
                    exam=exam, 
                    subdivision_id=s_data['subdivision_id'], 
                    title=s_data['title'],
                    instructions=s_data.get('instructions', ''), 
                    time_limit=s_data.get('time_limit', 0), 
                    order=idx
                )
                sections_map[s_data['subdivision_id']] = section
        
        # FASE DE LLENADO ATÓMICO (Bucle Iterativo por Sección)
        generated_titles = []
        usage_total = {"in": 0, "out": 0}
        
        for s_info in section_plan:
            db_sec = sections_map.get(s_info['subdivision_id'])
            if not db_sec: continue
            
            # Inyección de immersion_mode y pedagogical_level en el prompt atómico
            s_prompt = strategy.get_system_prompt(
                immersion_mode=exam.immersion_mode, 
                pedagogical_level=exam.pedagogical_level
            )
            u_prompt = strategy.get_user_prompt(
                context_text=context_text, topic=topic or subject.name,
                subdivision_id=s_info['subdivision_id'], generated_item_titles=generated_titles,
                immersion_mode=exam.immersion_mode, pedagogical_level=exam.pedagogical_level
            )
            
            success, resp, key_name, usage = generate_text_content(
                u_prompt, 
                system_instruction=s_prompt, 
                api_key=AutomationSettings.load().active_api_key, 
                response_schema=strategy.get_output_schema()
            )
            if success:
                usage_total["in"] += usage.get("input_tokens", 0)
                usage_total["out"] += usage.get("output_tokens", 0)
                items = dirtyjson.loads(clean_json_response(resp)).get("items", [])
                for i_idx, i_data in enumerate(items):
                    ExamItem.objects.create(
                        section=db_sec, 
                        block_type=i_data.get('block_type', 'UNKNOWN'),
                        widget_id=i_data.get('widget_id', 'UNKNOWN'), 
                        content=i_data.get('content', {}),
                        grading_logic=i_data.get('grading_logic', {}), 
                        metadata=i_data.get('metadata', {}), 
                        order=i_idx
                    )
                    generated_titles.append(str(i_data.get('content', {}).get('stem', ''))[:30])
                    time.sleep(5) # PROTECCIÓN CUOTA RPM (HITO 6)

        TrackingService.record_usage(exam.user, exam, "gemini-2.5-flash-lite", usage_total["in"], usage_total["out"], "Restored-Key")
        exam.status = 'READY'
        exam.expiration_date = timezone.now() + timedelta(hours=24)
        exam.event_log.append({"ts": timezone.now().isoformat(), "msg": "Generación Completada. Caduca en 24h."})
        exam.save()

    except MaxRetriesExceededError:
        if exam:
            exam.status = 'ERROR'
            exam.save()
            send_unified_notification(
                exam.user, 
                "Servicio de Clasificación no disponible", 
                "Servicio de Clasificación no disponible temporalmente. Por favor, inténtelo de nuevo más tarde.", 
                reverse('assessment_v2:dashboard')
            )
    except Exception as e:
        if isinstance(e, Retry): raise e
        if exam:
            exam.status = 'ERROR'
            exam.error_log = traceback.format_exc()
            exam.save()
