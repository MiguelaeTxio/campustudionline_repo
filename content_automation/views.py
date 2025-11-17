# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/content_automation/views.py
# El namespace de la app es 'content_automation'

import logging
from collections import defaultdict
import datetime
import json
import os
import re

from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count, F
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db import IntegrityError

from academic_structure.models import University, Branch, Degree, Subject
from contents.models import ContentMaterial, FreeContentSubCategory
from messaging.push_utils import send_notification_to_user
from .models import PendingContentTask, ContentRequest, FreeContentRequest
from orchestrator.models import AutomationSettings, ApiKey
from .forms import FreeCourseCreationForm, FreeContentRequestForm, RejectionReasonForm, ReviseTaskForm, SeedFiltersForm
from orchestrator.tasks import generate_full_course_task

logger = logging.getLogger(__name__)

# ==============================================================================
# Vistas del Panel de Control Unificado (Hito 3 / Hito 18 - FASE 5)
# ==============================================================================


@staff_member_required
def task_dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    [V3.3 - DIRECTRIZ MIGUEL ÁNGEL] Dashboard unificado.
    La clave en uso se obtiene del registro de la tarea activa ('PROCESSING'), no del estado global.
    """
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
    
    finalized_statuses = [
        PendingContentTask.StatusChoices.COMPLETED,
        PendingContentTask.StatusChoices.FAILED,
        PendingContentTask.StatusChoices.FAILED_FATAL
    ]
    active_tasks = PendingContentTask.objects.exclude(
        status__in=finalized_statuses
    ).select_related('subject', 'assigned_to').order_by('-created_at')
    
    in_progress_tasks_count = active_tasks.count()

    pending_requests = ContentRequest.objects.filter(
        status=ContentRequest.StatusChoices.PENDING
    ).annotate(requester_count=Count('requesters')).select_related('subject').order_by('-requester_count')

    # Identificar asignaturas que ya tienen una tarea activa
    subjects_with_active_tasks = set(
        PendingContentTask.objects.exclude(
            status__in=finalized_statuses
        ).values_list('subject_id', flat=True)
    )

    pending_free_requests = FreeContentRequest.objects.filter(
        status=FreeContentRequest.STATUS_PENDING
    ).select_related('requester').order_by('created_at')
    
    finished_tasks_qs = PendingContentTask.objects.filter(
        status__in=finalized_statuses
    ).select_related('subject', 'assigned_to').order_by('-updated_at')
    
    paginator = Paginator(finished_tasks_qs, 10)
    page_number = request.GET.get('page')
    finished_tasks_page = paginator.get_page(page_number)

    context.update({
        "title": "Centro de Control de Contenidos",
        "subtitle": "Panel de Control Integrado",
        "settings": settings_instance,
        "current_api_key_in_use": current_api_key_in_use,
        "academic_content_count": subjects_with_content_count,
        "total_academic_subjects": total_subjects_count,
        "academic_coverage_percentage": round(coverage_percentage, 2),
        "free_content_count": free_content_count,
        "pending_requests_count": pending_academic_requests_count + pending_free_requests_count,
        "in_progress_tasks_count": in_progress_tasks_count,
        "pending_requests": pending_requests,
        "subjects_with_active_tasks": subjects_with_active_tasks,
        "pending_free_requests": pending_free_requests,
        "active_tasks": active_tasks,
        "finished_tasks_page": finished_tasks_page,
    })
    return render(request, "admin/content_automation/dashboard.html", context)


@staff_member_required
def automation_control_view(request: HttpRequest) -> HttpResponse:
    context = admin.site.each_context(request)
    
    settings_instance = AutomationSettings.load()
    settings_instance.refresh_from_db()
    available_api_keys = ApiKey.objects.filter(is_enabled=True)
    seed_form = SeedFiltersForm(instance=settings_instance)

    generation_task_history = PendingContentTask.objects.select_related(
        'subject'
    ).order_by('-created_at')[:50]

    context.update({
        "title": "Centro de Control de Automatización",
        "subtitle": "Gestión de la Automatización Masiva",
        "settings": settings_instance,
        "available_api_keys": available_api_keys,
        "generation_task_history": generation_task_history,
        "seed_form": seed_form,
    })
    return render(request, "admin/content_automation/automation_control_center.html", context)


@staff_member_required
def get_academic_filters_htmx(request: HttpRequest) -> HttpResponse:
    branch_id = request.GET.get('branch')
    degree_id = request.GET.get('degree')

    if branch_id:
        degrees = Degree.objects.filter(branch_id=branch_id).order_by('name')
        return render(request, "admin/content_automation/partials/_degree_options.html", {"degrees": degrees})
    
    if degree_id:
        try:
            degree = Degree.objects.get(pk=degree_id)
            years = range(1, degree.duration_in_years + 1)
            year_map = {1: "Primero", 2: "Segundo", 3: "Tercero", 4: "Cuarto", 5: "Quinto"}
            year_choices = [year_map.get(y, str(y)) for y in years if y in year_map]
            return render(request, "admin/content_automation/partials/_year_options.html", {"years": year_choices})
        except (Degree.DoesNotExist, TypeError, ValueError):
            return HttpResponse("")

    return HttpResponse("")


@staff_member_required
def get_sub_categories_htmx(request: HttpRequest) -> HttpResponse:
    """
    [REFACTORIZADO] Vista HTMX para poblar el selector de subcategorías
    basado en la categoría maestra seleccionada.
    """
    master_id = request.GET.get('master_category')
    subcategories = FreeContentSubCategory.objects.none()
    if master_id:
        try:
            subcategories = FreeContentSubCategory.objects.filter(master_category_id=master_id).order_by('display_order', 'name')
        except (ValueError, TypeError):
            pass

    temp_form = FreeCourseCreationForm()
    temp_form.fields['sub_category'].queryset = subcategories
    
    return render(
        request,
        "admin/content_automation/partials/_category_options_form_row.html",
        {"field": temp_form['sub_category']}
    )


@staff_member_required
def task_log_full_page_view(request: HttpRequest, task_id: str) -> HttpResponse:
    context = admin.site.each_context(request)
    task = get_object_or_404(PendingContentTask, pk=task_id)
    log_entries = []

    if task.log_file_path and os.path.exists(task.log_file_path):
        try:
            with open(task.log_file_path, "r", encoding="utf-8") as f:
                log_content = f.read()

            pattern = re.compile(
                r"\[(.*?)\] \[(.*?)\] ([^\n]*)(?:\n--- PAYLOAD ---\n(.*?)\n-----------------\n)?",
                re.DOTALL
            )
            
            for match in pattern.finditer(log_content):
                timestamp, level, message, payload = match.groups()
                log_entries.append({
                    "timestamp": timestamp,
                    "level": level,
                    "message": message.strip(),
                    "payload": payload.strip() if payload else None
                })
        except Exception as e:
            logger.error(f"Error al leer o parsear el archivo de log {task.log_file_path}: {e}")
            messages.error(request, f"No se pudo leer el archivo de log. Error: {e}")
    
    context.update({
        "title": f"Log de Tarea: {task}",
        "task": task,
        "task_log_reversed": list(reversed(log_entries)),
        "subtitle": f"ID: {task.id}",
    })
    return render(request, "admin/content_automation/task_log_full_page.html", context)


# ==============================================================================
# Vistas de Creación de Tareas y Triage de Solicitudes
# ==============================================================================


@staff_member_required
def create_academic_task_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and "subject_id" in request.POST:
        subject = get_object_or_404(Subject, pk=request.POST.get("subject_id"))
        
        if subject.is_content_generation_locked():
            messages.error(
                request, f'La generación de contenido para "{subject.name}" está bloqueada (ya existe contenido o una tarea).'
            )
        else:
            task = PendingContentTask.objects.create(
                subject=subject, assigned_to=request.user
            )
            generate_full_course_task.delay(str(task.id))
            messages.success(
                request, f'Tarea para "{subject.name}" encolada con éxito.'
            )
        return HttpResponseRedirect(reverse("content_automation_admin:task_dashboard"))

    context = admin.site.each_context(request)
    context.update({"title": "Crear Tarea desde Asignatura"})
    
    breadcrumbs = [
        {"name": "Centro de Control", "url": reverse("content_automation_admin:task_dashboard")},
        {"name": "Crear Tarea Académica", "url": ""},
    ]
    parent_url, item_type, page_obj = None, "university", None
    
    if "degree_id" in request.GET:
        item_type = "subject"
        degree = get_object_or_404(Degree.objects.select_related("branch__university"), pk=request.GET["degree_id"])
        parent_url = f"{reverse('content_automation_admin:create_academic_task')}?branch_id={degree.branch.pk}"
        breadcrumbs.extend([
            {"name": degree.branch.university.name, "url": f"{reverse('content_automation_admin:create_academic_task')}?university_id={degree.branch.university.pk}"},
            {"name": degree.branch.name, "url": parent_url},
            {"name": degree.name, "url": ""},
        ])
        subjects_by_year = defaultdict(list)
        
        query = Subject.objects.filter(academic_year__degree=degree).select_related('academic_year').order_by("academic_year__year", "name")
        
        for subject in query:
            subject.is_locked = subject.is_content_generation_locked()
            subjects_by_year[subject.academic_year.year].append(subject)
        context["subjects_grouped_by_year"] = dict(sorted(subjects_by_year.items()))
    else:
        if "branch_id" in request.GET:
            item_type = "degree"
            branch = get_object_or_404(Branch.objects.select_related("university"), pk=request.GET["branch_id"])
            queryset = Degree.objects.filter(branch=branch).order_by("name")
            parent_url = f"{reverse('content_automation_admin:create_academic_task')}?university_id={branch.university.pk}"
            breadcrumbs.extend([
                {"name": branch.university.name, "url": parent_url},
                {"name": branch.name, "url": ""},
            ])
        elif "university_id" in request.GET:
            item_type = "branch"
            university = get_object_or_404(University, pk=request.GET["university_id"])
            queryset = Branch.objects.filter(university=university).order_by("name")
            parent_url = reverse("content_automation_admin:create_academic_task")
            breadcrumbs.append({"name": university.name, "url": ""})
        else:
            item_type = "university"
            queryset = University.objects.all().order_by("name")
        paginator = Paginator(queryset, 25)
        page_obj = paginator.get_page(request.GET.get("page"))

    context.update({
        "item_type": item_type,
        "breadcrumbs": breadcrumbs,
        "parent_url": parent_url,
        "page_obj": page_obj,
    })
    return render(request, "admin/content_automation/create_academic_task.html", context)


@staff_member_required
def create_free_task_view(request: HttpRequest) -> HttpResponse:
    """
    [REFACTORIZADO] Vista para crear tareas de contenido libre.
    1. Valida los datos del nuevo formulario de servicio.
    2. Crea el objeto PendingContentTask con la clasificación manual en structured_content.
    3. Encola la tarea de Celery.
    """
    if request.method == "POST":
        form = FreeCourseCreationForm(request.POST)
        if form.is_valid():
            try:
                title = form.cleaned_data['course_title']
                prompt = form.cleaned_data['prompt_text']
                master_category = form.cleaned_data['master_category']
                sub_category = form.cleaned_data.get('sub_category')

                # Preparamos el payload de clasificación para la tarea de Celery
                manual_classification = {
                    'master_category_id': str(master_category.id),
                    'sub_category_id': str(sub_category.id) if sub_category else None,
                }

                task = PendingContentTask.objects.create(
                    course_title=title,
                    prompt_text=prompt,
                    assigned_to=request.user,
                    task_origin=PendingContentTask.TaskOrigin.MANUAL_CREATION,
                    structured_content={'manual_classification': manual_classification}
                )
                
                generate_full_course_task.delay(str(task.id))
                
                source_request_id = request.POST.get('source_request_id')
                if source_request_id:
                    try:
                        original_request = FreeContentRequest.objects.get(pk=source_request_id)
                        original_request.status = FreeContentRequest.STATUS_APPROVED
                        original_request.save(update_fields=['status'])
                        messages.success(request, f'La solicitud "{original_request.title}" ha sido aprobada y la tarea de generación ha sido encolada.')
                    except FreeContentRequest.DoesNotExist:
                        logger.warning(f"Se intentó aprobar la solicitud {source_request_id} pero no se encontró.")
                else:
                    messages.success(request, f'La tarea para el curso libre "{task.course_title}" ha sido encolada con éxito.')

            except IntegrityError:
                messages.error(request, f'Error: Ya existe una tarea de generación activa para un curso con el título "{title}".')

            return HttpResponseRedirect(reverse("content_automation_admin:task_dashboard"))
    else:
        context = admin.site.each_context(request)
        request_id = request.GET.get('request_id')
        reject_url = None
        source_request = None
        
        if request_id:
            source_request = get_object_or_404(FreeContentRequest, pk=request_id)
            initial_data = {'course_title': source_request.title, 'prompt_text': source_request.detailed_prompt}
            form = FreeCourseCreationForm(initial=initial_data)
            title = f"Revisar Solicitud: \"{source_request.title}\""
            subtitle = "Aprobar y clasificar una solicitud de usuario."
            breadcrumbs = [
                {"name": "Centro de Control", "url": reverse("content_automation_admin:task_dashboard")},
                {"name": "Revisar Solicitud", "url": ""},
            ]
            reject_url = reverse('content_automation_admin:reject_free_request', args=[source_request.pk])
        else:
            form = FreeCourseCreationForm()
            title = "Crear Tarea para Curso Libre"
            subtitle = "Generar un nuevo material de contenido no vinculado a la estructura académica."
            breadcrumbs = [
                {"name": "Centro de Control", "url": reverse("content_automation_admin:task_dashboard")},
                {"name": "Crear Tarea Libre", "url": ""},
            ]

        context.update({
            "title": title,
            "subtitle": subtitle,
            "form": form,
            "source_request": source_request,
            "reject_url": reject_url,
            "breadcrumbs": breadcrumbs,
        })
        return render(request, "admin/content_automation/create_free_task.html", context)


# ==============================================================================
# Endpoints de Acción (POST only / Vistas de triage)
# ==============================================================================
@require_POST
@staff_member_required
def set_seed_filters_view(request: HttpRequest) -> HttpResponse:
    settings_instance = AutomationSettings.load()
    form = SeedFiltersForm(instance=settings_instance, data=request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Los filtros de semilla han sido actualizados.")
    else:
        error_str = "; ".join([f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()])
        messages.error(request, f"Hubo un error al guardar los filtros: {error_str}")
    return HttpResponseRedirect(reverse("content_automation_admin:automation_control_center"))


@require_POST
@staff_member_required
def toggle_automation_status_view(request: HttpRequest) -> HttpResponse:
    settings_instance = AutomationSettings.load()
    settings_instance.is_running = not settings_instance.is_running
    settings_instance.save(update_fields=['is_running'])
    settings_instance.refresh_from_db()
    return render(request, "admin/content_automation/_automation_control_panel.html", {"settings": settings_instance})


@require_POST
@staff_member_required
def set_active_api_key_view(request: HttpRequest) -> HttpResponse:
    api_key_id = request.POST.get('api_key')
    settings_instance = AutomationSettings.load()
    if api_key_id:
        try:
            api_key = ApiKey.objects.get(pk=api_key_id, is_enabled=True)
            settings_instance.active_api_key = api_key
            settings_instance.save(update_fields=['active_api_key'])
            messages.success(request, f'La clave de API "{api_key.name}" ha sido activada.')
        except ApiKey.DoesNotExist:
            messages.error(request, "La clave de API seleccionada no es válida o no está habilitada.")
    else:
        settings_instance.active_api_key = None
        settings_instance.save(update_fields=['active_api_key'])
        messages.warning(request, "No hay ninguna clave de API activa asignada.")
    next_url = request.POST.get('next', reverse('content_automation_admin:task_dashboard'))
    return HttpResponseRedirect(next_url)


@require_POST
@staff_member_required
def pause_task_view(request: HttpRequest, task_id: str) -> HttpResponse:
    task = get_object_or_404(PendingContentTask, pk=task_id)
    if task.status == PendingContentTask.StatusChoices.PROCESSING:
        task.status = PendingContentTask.StatusChoices.PAUSED
        task.save(update_fields=["status"])
    return render(request, "admin/content_automation/_task_row.html", {"task": task})


@require_POST
@staff_member_required
def resume_task_view(request: HttpRequest, task_id: str) -> HttpResponse:
    task = get_object_or_404(PendingContentTask, pk=task_id)
    if task.status == PendingContentTask.StatusChoices.PAUSED:
        task.status = PendingContentTask.StatusChoices.PENDING
        task.save(update_fields=["status"])
        generate_full_course_task.delay(str(task.id))
    return render(request, "admin/content_automation/_task_row.html", {"task": task})


@require_POST
@staff_member_required
def cancel_task_view(request: HttpRequest, task_id: str) -> HttpResponse:
    task = get_object_or_404(PendingContentTask, pk=task_id)
    if task.status not in [PendingContentTask.StatusChoices.COMPLETED, PendingContentTask.StatusChoices.FAILED, PendingContentTask.StatusChoices.FAILED_FATAL]:
        task.status = PendingContentTask.StatusChoices.FAILED
        task.notes = "Tarea cancelada manualmente por el administrador."
        task.save(update_fields=["status", "notes"])
    return render(request, "admin/content_automation/_task_row.html", {"task": task})


@staff_member_required
def task_row_partial_view(request: HttpRequest, task_id: str) -> HttpResponse:
    task = get_object_or_404(PendingContentTask, pk=task_id)
    return render(request, "admin/content_automation/_task_row.html", {"task": task})


@staff_member_required
def get_modal_log_content_view(request: HttpRequest, task_id: str) -> HttpResponse:
    task = get_object_or_404(PendingContentTask, pk=task_id)
    return render(request, "admin/content_automation/_task_log_modal_content.html", {"task": task, "task_log_reversed": []})


@staff_member_required
def get_automation_status_view(request: HttpRequest) -> HttpResponse:
    settings_instance = AutomationSettings.load()
    return render(request, "admin/content_automation/_automation_stats.html", {"settings": settings_instance})


@staff_member_required
def reject_free_request_view(request: HttpRequest, request_id: str) -> HttpResponse:
    free_request = get_object_or_404(FreeContentRequest, pk=request_id)
    form = RejectionReasonForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        return HttpResponseRedirect(reverse('content_automation_admin:task_dashboard'))
    context = admin.site.each_context(request)
    context.update({"form": form, "free_request": free_request})
    return render(request, "admin/content_automation/reject_request_form.html", context)


@staff_member_required
def delete_free_request_view(request: HttpRequest, request_id: str) -> HttpResponse:
    free_request = get_object_or_404(FreeContentRequest, pk=request_id)
    if request.method == 'POST':
        free_request.delete()
        return HttpResponseRedirect(reverse('content_automation_admin:task_dashboard'))
    context = admin.site.each_context(request)
    context.update({"free_request": free_request})
    return render(request, "admin/content_automation/confirm_request_deletion.html", context)


@staff_member_required
def manage_logs_view(request: HttpRequest) -> HttpResponse:
    context = admin.site.each_context(request)
    return render(request, "admin/content_automation/manage_logs.html", context)


@login_required
def request_free_content_view(request: HttpRequest) -> HttpResponse:
    form = FreeContentRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        return HttpResponseRedirect(reverse("search:search_home"))
    return render(request, "content_automation/request_free_content.html", {"form": form})


@staff_member_required
def revise_and_regenerate_view(request: HttpRequest, task_id: str) -> HttpResponse:
    task = get_object_or_404(PendingContentTask, pk=task_id)
    form = ReviseTaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        return HttpResponseRedirect(reverse("content_automation_admin:task_dashboard"))
    context = admin.site.each_context(request)
    context.update({"form": form, "task": task})
    return render(request, "admin/content_automation/revise_task_form.html", context)
