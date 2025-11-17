# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/admin_views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages, admin
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Assessment

@staff_member_required
def assessment_dashboard(request):
    """
    Muestra un panel de control con métricas y estados del sistema de autoevaluaciones,
    siguiendo los requisitos especificados.
    """
    context = admin.site.each_context(request)
    now = timezone.now()
    
    # --- 1. MÉTRICAS ---
    completed_assessments = Assessment.objects.filter(status=Assessment.AssessmentStatus.COMPLETED)
    
    # Métricas temporales
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=now.weekday())
    month_start = today_start.replace(day=1)
    year_start = month_start.replace(month=1)

    metrics = {
        'today': completed_assessments.filter(created_at__gte=today_start).count(),
        'week': completed_assessments.filter(created_at__gte=week_start).count(),
        'month': completed_assessments.filter(created_at__gte=month_start).count(),
        'year': completed_assessments.filter(created_at__gte=year_start).count(),
        'total': completed_assessments.count()
    }

    # --- 2. ESTADO DE TAREAS ---
    
    # Tarea actualmente en proceso (debería ser solo una)
    processing_task = Assessment.objects.filter(
        status=Assessment.AssessmentStatus.PROCESSING
    ).order_by('created_at').first()

    # Tareas encoladas, listas para ser procesadas
    pending_tasks = Assessment.objects.filter(
        status=Assessment.AssessmentStatus.PENDING
    ).order_by('created_at')

    # Últimas 10 tareas finalizadas (completadas o fallidas)
    finished_tasks = Assessment.objects.exclude(
        status__in=[
            Assessment.AssessmentStatus.PENDING,
            Assessment.AssessmentStatus.PROCESSING
        ]
    ).order_by('-created_at')[:10]

    context.update({
        'title': 'Panel de Control de Evaluaciones',
        'metrics': metrics,
        'processing_task': processing_task,
        'pending_tasks': pending_tasks,
        'finished_tasks': finished_tasks,
    })
    return render(request, 'admin/assessment/dashboard.html', context)

@staff_member_required
def pause_assessment_task(request, pk):
    """Pausa una tarea de evaluación que está en proceso."""
    task = get_object_or_404(Assessment, pk=pk)
    if task.status == Assessment.AssessmentStatus.PROCESSING:
        task.status = Assessment.AssessmentStatus.PAUSED
        task.save()
        messages.success(request, f"La tarea de evaluación #{task.pk} ha sido pausada.")
    else:
        messages.warning(request, f"La tarea #{task.pk} no se puede pausar porque no está en proceso.")
    return redirect(reverse('admin:assessment_admin:assessment_dashboard'))

@staff_member_required
def resume_assessment_task(request, pk):
    """Reanuda una tarea de evaluación pausada."""
    task = get_object_or_404(Assessment, pk=pk)
    if task.status == Assessment.AssessmentStatus.PAUSED:
        # Se devuelve a PENDING para que el orquestador la recoja en el siguiente ciclo.
        task.status = Assessment.AssessmentStatus.PENDING
        task.save()
        messages.success(request, f"La tarea de evaluación #{task.pk} ha sido reanudada y puesta en cola.")
    else:
        messages.warning(request, f"La tarea #{task.pk} no se puede reanudar porque no está pausada.")
    return redirect(reverse('admin:assessment_admin:assessment_dashboard'))

@staff_member_required
def cancel_assessment_task(request, pk):
    """Cancela una tarea de evaluación que esté pendiente o pausada."""
    task = get_object_or_404(Assessment, pk=pk)
    if task.status in [Assessment.AssessmentStatus.PENDING, Assessment.AssessmentStatus.PAUSED]:
        task.status = Assessment.AssessmentStatus.CANCELLED
        task.save()
        messages.success(request, f"La tarea de evaluación #{task.pk} ha sido cancelada.")
    else:
        messages.error(request, f"La tarea #{task.pk} no se puede cancelar. Solo tareas pendientes o pausadas son cancelables.")
    return redirect(reverse('admin:assessment_admin:assessment_dashboard'))

@staff_member_required
def view_assessment_log(request, pk):
    """Muestra los logs detallados para una tarea de evaluación específica."""
    task = get_object_or_404(Assessment, pk=pk)
    
    # Obtener el contexto base del sitio de administración para que la plantilla herede correctamente.
    context = admin.site.each_context(request)
    
    # Añadir nuestras variables específicas al contexto.
    context.update({
        'title': f'Log de la Evaluación #{task.pk}',
        'subtitle': f'Detalles para la tarea de {task.user.username}',
        'task': task,
        'opts': Assessment._meta, # Necesario para algunas partes de las plantillas admin.
    })
    
    return render(request, 'admin/assessment/view_log.html', context)
