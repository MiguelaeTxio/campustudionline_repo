# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/admin_views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin, messages
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models.main import Exam
from datetime import timedelta

@staff_member_required
def assessment_dashboard_view(request):
    """
    Vista personalizada para el Dashboard de Evaluaciones V2.
    Recupera métricas de exámenes y estado de las colas.
    """
    context = admin.site.each_context(request)
    now = timezone.now()
    
    # Métricas adaptadas
    metrics = {
        'today': Exam.objects.filter(status='GRADED', updated_at__date=now.date()).count(),
        'week': Exam.objects.filter(status='GRADED', updated_at__gt=now - timedelta(days=7)).count(),
        'total': Exam.objects.filter(status='GRADED').count(),
    }

    processing_task = Exam.objects.filter(status__in=['GENERATING', 'GRADING']).first()
    pending_tasks = Exam.objects.filter(status='PENDING').order_by('created_at')[:10]
    finished_tasks = Exam.objects.exclude(status__in=['PENDING', 'GENERATING', 'GRADING']).order_by('-updated_at')[:10]

    context.update({
        'title': 'Centro de Control de Evaluaciones (V2)',
        'metrics': metrics,
        'processing_task': processing_task,
        'pending_tasks': pending_tasks,
        'finished_tasks': finished_tasks,
    })
    return render(request, 'admin/assessment_v2/dashboard.html', context)

@staff_member_required
def pause_exam_task(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    # Lógica de pausa (Placeholder para integración con Celery)
    messages.info(request, f"Examen {exam.uuid} marcado para revisión.")
    # [FIXED] Redirección corregida al namespace del dashboard interactivo
    return HttpResponseRedirect(reverse('assessment_admin:assessment_dashboard'))


@staff_member_required
def get_exam_log_content_view(request, pk):
    """
    Devuelve el fragmento HTML con el log de eventos del examen para el modal.
    """
    exam = get_object_or_404(Exam, pk=pk)
    # Invertimos el log para ver lo más reciente arriba
    event_log_reversed = list(reversed(exam.event_log or []))
    
    return render(request, "admin/assessment_v2/_exam_log_modal_content.html", {
        "exam": exam,
        "event_log_reversed": event_log_reversed
    })
