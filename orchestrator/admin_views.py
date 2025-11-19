# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/admin_views.py
import logging
from collections import defaultdict
import os
import re

from django.contrib import messages
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db import IntegrityError

from academic_structure.models import Degree, Subject, Branch, University
from contents.models import ContentMaterial, FreeContentSubCategory
from .models import PendingContentTask, ContentRequest, FreeContentRequest, AutomationSettings, ApiKey
from .forms import FreeCourseCreationForm, RejectionReasonForm, ReviseTaskForm, SeedFiltersForm
from .tasks import generate_full_course_task

logger = logging.getLogger(__name__)

@staff_member_required
def task_dashboard_view(request: HttpRequest) -> HttpResponse:
    context = admin.site.each_context(request)
    settings_instance = AutomationSettings.load()
    active_task_in_progress = PendingContentTask.objects.filter(status=PendingContentTask.StatusChoices.PROCESSING).first()
    current_api_key_in_use = active_task_in_progress.api_key_used if active_task_in_progress else "Ninguna tarea en proceso"
    total_subjects_count = Subject.objects.count()
    subjects_with_content_count = Subject.objects.filter(content_materials__isnull=False).count()
    coverage_percentage = (subjects_with_content_count / total_subjects_count) * 100 if total_subjects_count > 0 else 0
    free_content_count = ContentMaterial.objects.filter(subject__isnull=True).count()
    pending_academic_requests_count = ContentRequest.objects.filter(status=ContentRequest.StatusChoices.PENDING).count()
    pending_free_requests_count = FreeContentRequest.objects.filter(status=FreeContentRequest.STATUS_PENDING).count()
    finalized_statuses = [PendingContentTask.StatusChoices.COMPLETED, PendingContentTask.StatusChoices.FAILED, PendingContentTask.StatusChoices.FAILED_FATAL]
    active_tasks = PendingContentTask.objects.exclude(status__in=finalized_statuses).select_related('subject', 'assigned_to').order_by('-created_at')
    in_progress_tasks_count = active_tasks.count()
    pending_requests = ContentRequest.objects.filter(status=ContentRequest.StatusChoices.PENDING).annotate(requester_count=Count('requesters')).select_related('subject').order_by('-requester_count')
    subjects_with_active_tasks = set(PendingContentTask.objects.exclude(status__in=finalized_statuses).values_list('subject_id', flat=True))
    pending_free_requests = FreeContentRequest.objects.filter(status=FreeContentRequest.STATUS_PENDING).select_related('requester').order_by('created_at')
    finished_tasks_qs = PendingContentTask.objects.filter(status__in=finalized_statuses).select_related('subject', 'assigned_to').order_by('-updated_at')
    paginator = Paginator(finished_tasks_qs, 10)
    page_number = request.GET.get('page')
    finished_tasks_page = paginator.get_page(page_number)
    context.update({
        "title": "Centro de Control de Contenidos", "subtitle": "Panel de Control Integrado", "settings": settings_instance,
        "current_api_key_in_use": current_api_key_in_use, "academic_content_count": subjects_with_content_count,
        "total_academic_subjects": total_subjects_count, "academic_coverage_percentage": round(coverage_percentage, 2),
        "free_content_count": free_content_count, "pending_requests_count": pending_academic_requests_count + pending_free_requests_count,
        "in_progress_tasks_count": in_progress_tasks_count, "pending_requests": pending_requests,
        "subjects_with_active_tasks": subjects_with_active_tasks, "pending_free_requests": pending_free_requests,
        "active_tasks": active_tasks, "finished_tasks_page": finished_tasks_page,
    })
    return render(request, "admin/orchestrator/dashboard.html", context)

@staff_member_required
def automation_control_view(request: HttpRequest) -> HttpResponse:
    context = admin.site.each_context(request)
    settings_instance = AutomationSettings.load()

    if request.method == "POST":
        seed_form = SeedFiltersForm(request.POST, instance=settings_instance)
        if seed_form.is_valid():
            seed_form.save()
            messages.success(request, "Los filtros de semilla se han guardado correctamente.")
            return HttpResponseRedirect(reverse("orchestrator:automation_control_center"))
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        seed_form = SeedFiltersForm(instance=settings_instance)

    generation_task_history = PendingContentTask.objects.order_by("-created_at")[:50]

    context.update({
        "title": "Centro de Control de Automatización",
        "settings": settings_instance,
        "seed_form": seed_form,
        "generation_task_history": generation_task_history,
    })
    return render(request, "admin/orchestrator/automation_control_center.html", context)

@staff_member_required
def get_automation_status_view(request: HttpRequest) -> HttpResponse:
    settings_instance = AutomationSettings.load()
    context = {"settings": settings_instance}
    return render(request, "admin/orchestrator/_automation_status_panel.html", context)

@staff_member_required
def get_academic_filters_htmx(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def get_sub_categories_htmx(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def task_log_full_page_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def create_academic_task_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def create_free_task_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def set_seed_filters_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def toggle_automation_status_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def set_active_api_key_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def pause_task_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def resume_task_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def cancel_task_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def task_row_partial_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def get_modal_log_content_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def reject_free_request_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def delete_free_request_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def manage_logs_view(request, *args, **kwargs): return HttpResponse("Placeholder")
@staff_member_required
def revise_and_regenerate_view(request, *args, **kwargs): return HttpResponse("Placeholder")
