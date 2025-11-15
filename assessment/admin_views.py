# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/admin_views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
import json

from .models import Assessment, AssessmentSettings
from .tasks import generate_assessment_from_content_task, correct_assessment_task

def log_engine_event(message, level="INFO"):
    """Helper para registrar eventos en el log del motor de evaluaciones."""
    settings = AssessmentSettings.get_settings()
    log_entry = {
        "timestamp": timezone.now().isoformat(),
        "level": level,
        "message": message,
    }
    # Mantener el log con un tamaño razonable
    if len(settings.event_log) > 100:
        settings.event_log = settings.event_log[-100:]
    settings.event_log.append(log_entry)
    settings.save(update_fields=["event_log"])

@staff_member_required
def assessment_dashboard(request):
    """
    Vista principal del dashboard de administración del motor de evaluaciones.
    """
    settings = AssessmentSettings.get_settings()
    
    # Estadísticas
    status_counts = dict(
        Assessment.objects.values_list("status").annotate(count=Count("status"))
    )
    stats = {
        choice: status_counts.get(key, 0)
        for key, choice in Assessment.AssessmentStatus.choices
    }

    # Tareas en curso y fallidas
    processing_tasks = Assessment.objects.filter(
        status__in=[
            Assessment.AssessmentStatus.PROCESSING,
            Assessment.AssessmentStatus.CORRECTING,
        ]
    ).order_by("-created_at")

    failed_tasks = Assessment.objects.filter(
        status__in=[
            Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE,
            Assessment.AssessmentStatus.CORRECTION_FAILED_RETRYABLE,
        ]
    ).order_by("-created_at")

    paused_tasks = Assessment.objects.filter(
        status=Assessment.AssessmentStatus.PAUSED
    ).order_by("-created_at")

    context = {
        "title": "Centro de Control de Evaluaciones",
        "settings": settings,
        "stats": stats,
        "processing_tasks": processing_tasks,
        "failed_tasks": failed_tasks,
        "paused_tasks": paused_tasks,
        "event_log_pretty": json.dumps(settings.event_log, indent=2, ensure_ascii=False),
        "app_label": "assessment",
    }
    return render(request, "admin/assessment/dashboard.html", context)

@staff_member_required
def toggle_assessment_engine(request):
    """
    Inicia o detiene el motor de evaluaciones.
    """
    if request.method == "POST":
        settings = AssessmentSettings.get_settings()
        settings.is_running = not settings.is_running
        settings.save(update_fields=["is_running"])
        action = "iniciado" if settings.is_running else "detenido"
        log_engine_event(f"El motor ha sido {action} por {request.user.username}.")
        messages.success(request, f"El motor de evaluaciones ha sido {action}.")
    return redirect("admin:assessment_dashboard")

@staff_member_required
def pause_assessment_task(request, pk):
    """
    Pausa una tarea de evaluación específica que está en proceso.
    """
    task = get_object_or_404(Assessment, pk=pk)
    if task.status in [
        Assessment.AssessmentStatus.PROCESSING,
        Assessment.AssessmentStatus.CORRECTING,
    ]:
        task.status = Assessment.AssessmentStatus.PAUSED
        task.save(update_fields=["status"])
        messages.success(request, f"La tarea {pk} ha sido pausada.")
    else:
        messages.warning(request, f"La tarea {pk} no está en un estado que permita ser pausada.")
    return redirect("admin:assessment_dashboard")

@staff_member_required
def resume_assessment_task(request, pk):
    """
    Reanuda una tarea pausada, devolviéndola a su estado original para ser retomada.
    """
    task = get_object_or_404(Assessment, pk=pk)
    if task.status == Assessment.AssessmentStatus.PAUSED:
        # Revertir al estado 'pendiente' para que el orquestador la recoja
        task.status = Assessment.AssessmentStatus.PENDING
        task.save(update_fields=["status"])
        
        # Re-encolar la tarea correspondiente
        if task.questions.exists(): # Si ya tiene preguntas, es una tarea de corrección
            correct_assessment_task.delay(task.id)
        else: # Si no, es de generación
            generate_assessment_from_content_task.delay(task.id)
            
        messages.success(request, f"La tarea {pk} ha sido reanudada y encolada.")
    else:
        messages.warning(request, f"La tarea {pk} no está en estado 'Pausada'.")
    return redirect("admin:assessment_dashboard")

@staff_member_required
def retry_failed_task(request, pk):
    """
    Reintenta manualmente una tarea que ha fallado.
    """
    task = get_object_or_404(Assessment, pk=pk)
    if task.status in [
        Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE,
        Assessment.AssessmentStatus.CORRECTION_FAILED_RETRYABLE,
    ]:
        # El estado se deja como está, solo se re-encola la tarea
        if task.status == Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE:
            generate_assessment_from_content_task.delay(task.id)
            msg = f"Re-encolada tarea de GENERACIÓN {pk}."
        else:
            correct_assessment_task.delay(task.id)
            msg = f"Re-encolada tarea de CORRECCIÓN {pk}."
        
        log_engine_event(f"Reintento manual para la tarea {pk} solicitado por {request.user.username}.")
        messages.success(request, msg)
    else:
        messages.warning(request, "Esta tarea no está en un estado de fallo reintentable.")
    return redirect("admin:assessment_dashboard")

