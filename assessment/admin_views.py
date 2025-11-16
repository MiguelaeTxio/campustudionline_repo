# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/admin_views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Assessment

@staff_member_required
def assessment_dashboard(request):
    """
    Muestra un panel de control con métricas y estados del sistema de autoevaluaciones,
    siguiendo los requisitos especificados.
    """
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

    context = {
        'title': 'Panel de Control de Evaluaciones',
        'metrics': metrics,
        'processing_task': processing_task,
        'pending_tasks': pending_tasks,
        'finished_tasks': finished_tasks,
    }
    return render(request, 'admin/assessment/dashboard.html', context)
