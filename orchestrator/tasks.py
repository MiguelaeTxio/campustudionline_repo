# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/tasks.py
import logging
import traceback
import os
from datetime import datetime, timedelta
import pytz

from celery import shared_task
from django import db
from django.db import transaction
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from .models import AutomationSettings, ApiKey
from content_automation.models import PendingContentTask, ContentRequest
from academic_structure.models import Subject
from users.models import CustomUser
from content_automation.tasks import generate_full_course_task

# [PASO 5] Importaciones para el rescate de tareas de assessment
from assessment.models import Assessment
from assessment.tasks import generate_assessment_from_content_task, correct_assessment_task

logger = logging.getLogger(__name__)

QUARANTINE_MAILBOX_FILE = "/home/MiguelAeTxio/SWAP/quarantine_requests.log"

# --- Funciones Auxiliares de Orquestación ---

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

        dashboard_url = reverse("content_automation_admin:task_dashboard")
        
        email_subject = f"[CampuStudiOnline Automation] {title}"
        recipient_list = [admin.email for admin in admins]
        send_mail(
            subject=email_subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=True,
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

# --- Tarea Principal de Orquestación ---

@shared_task(bind=True)
def global_orchestrator_task(self):
    """
    [ORQUESTRADOR GLOBAL] Bucle principal que gestiona el estado del sistema y lanza tareas.
    """
    raise ValueError("AUDIT_ERROR_TIMESTAMP_21_30")
    try:
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

        # --- RESCATE DE TAREAS ZOMBIE ---
        zombie_threshold = timezone.now() - timedelta(minutes=5)
        zombie_tasks = PendingContentTask.objects.filter(status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.PENDING], created_at__lt=zombie_threshold)
        for task in zombie_tasks:
            message = f"VIGILANTE (CONTENT): Tarea '{task.id}' detectada como ZOMBIE. Marcada para rescate."
            _log_structured_event(message, "WARNING", {"task_id": str(task.id)})
            task.status = PendingContentTask.StatusChoices.FAILED_RETRYABLE
            task.save(update_fields=["status"])

        # --- [PASO 5] RESCATE DE TAREAS DE EVALUACIÓN ---
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
            # No hay estado intermedio, simplemente se re-encola. El estado FAILED_RETRYABLE es suficiente.
            correct_assessment_task.delay(assessment_corr_to_rescue.id)
            return

        # --- RESCATE DE TAREAS DE CONTENIDO FALLIDAS ---
        task_to_rescue = PendingContentTask.objects.filter(status__in=[PendingContentTask.StatusChoices.FAILED_RETRYABLE, PendingContentTask.StatusChoices.FAILED_QUOTA]).order_by('created_at').first()
        if task_to_rescue:
            _log_structured_event(f"RESCATE (CONTENT): Re-encolando la tarea de contenido {task_to_rescue.id}.")
            task_to_rescue.status = PendingContentTask.StatusChoices.PENDING
            task_to_rescue.save(update_fields=["status"])
            generate_full_course_task.delay(str(task_to_rescue.id))
            status_msg = f"AUTO-RECUPERACIÓN: Tarea para '{task_to_rescue}' re-encolada."
            automation_settings.last_run_status = status_msg
            automation_settings.last_run_timestamp = timezone.now()
            automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
            return

        if PendingContentTask.objects.filter(status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.PENDING]).exists():
            status_msg = "EN ESPERA: Hay una tarea de contenido en proceso o pendiente."
            if automation_settings.last_run_status != status_msg:
                _log_structured_event(status_msg, "INFO")
                automation_settings.last_run_status = status_msg
                automation_settings.save(update_fields=['last_run_status'])
            return

        # --- BÚSQUEDA DE NUEVO TRABAJO ---
        while True:
            subject_to_process = None
            approved_request = ContentRequest.objects.filter(status=ContentRequest.StatusChoices.APPROVED).order_by('created_at').first()
            if approved_request and approved_request.subject.content_materials.count() == 0:
                subject_to_process = approved_request.subject
                origin = PendingContentTask.TaskOrigin.APPROVED_REQUEST
                with transaction.atomic():
                    req = ContentRequest.objects.select_for_update().get(id=approved_request.id)
                    req.status = ContentRequest.StatusChoices.IN_PROGRESS
                    req.save(update_fields=["status"])
                _log_structured_event(f"PRIORIDAD: Reclamada la solicitud para '{subject_to_process.name}'.")
            
            if not subject_to_process:
                subject_qs = _get_next_subject_queryset(automation_settings)
                subject_to_process = subject_qs.order_by('?').first()
                if subject_to_process:
                    origin = PendingContentTask.TaskOrigin.MASS_GENERATION

            if subject_to_process:
                admin_user = CustomUser.objects.filter(is_superuser=True, is_active=True).order_by('pk').first()
                if not admin_user:
                    _log_structured_event("CRÍTICO: No se encontró un superusuario para asignar la tarea.", "CRITICAL")
                    raise Exception("No se encontró un superusuario para asignar la tarea.")
                
                new_task = PendingContentTask.objects.create(subject=subject_to_process, assigned_to=admin_user, task_origin=origin)
                
                log_msg = f"LANZADA: Tarea para el grupo '{subject_to_process.name}' (representante ID: {subject_to_process.id})."
                _log_structured_event(log_msg, "INFO", {"task_id": str(new_task.id)})
                generate_full_course_task.delay(str(new_task.id))
                status_msg = f"TAREA LANZADA: '{subject_to_process.name}' (ID: {new_task.id})."
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
