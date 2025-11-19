# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/admin_views.py
import logging
from collections import defaultdict
import os
import re
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST, require_http_methods
from django.db import IntegrityError

from academic_structure.models import Degree, Subject, Branch, University, AcademicYear
from contents.models import ContentMaterial, FreeContentSubCategory, FreeContentMasterCategory
from .models import PendingContentTask, ContentRequest, FreeContentRequest, AutomationSettings, ApiKey
from .forms import FreeCourseCreationForm, RejectionReasonForm, ReviseTaskForm, SeedFiltersForm
from .tasks import generate_full_course_task

logger = logging.getLogger(__name__)

# Directorio donde se almacenan los logs de las tareas Celery.
# Se define aquí para ser consistente a través de las vistas.
LOG_DIRECTORY = os.path.join(settings.BASE_DIR, '..', 'logs')


@staff_member_required
def task_dashboard_view(request: HttpRequest) -> HttpResponse:
    context = admin.site.each_context(request)
    settings_instance = AutomationSettings.load()
    active_task_in_progress = PendingContentTask.objects.filter(status=PendingContentTask.StatusChoices.PROCESSING).first()
    current_api_key_in_use = active_task_in_progress.api_key_used if active_task_in_progress else "Ninguna tarea en proceso"
    total_subjects_count = Subject.objects.count()
    subjects_with_content_count = Subject.objects.filter(content_hash_family__content_material__isnull=False).distinct().count()
    coverage_percentage = (subjects_with_content_count / total_subjects_count) * 100 if total_subjects_count > 0 else 0
    free_content_count = ContentMaterial.objects.filter(is_free_content=True).count()
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
    api_keys = ApiKey.objects.all()

    context.update({
        "title": "Centro de Control de Automatización",
        "settings": settings_instance,
        "seed_form": seed_form,
        "generation_task_history": generation_task_history,
        "api_keys": api_keys,
    })
    return render(request, "admin/orchestrator/automation_control_center.html", context)

@staff_member_required
def get_automation_status_view(request: HttpRequest) -> HttpResponse:
    settings_instance = AutomationSettings.load()
    context = {"settings": settings_instance}
    return render(request, "admin/orchestrator/_automation_status_panel.html", context)

@staff_member_required
def get_academic_filters_htmx(request):
    branch_id = request.GET.get('branch_id')
    degree_id = request.GET.get('degree_id')
    
    degrees = Degree.objects.none()
    years = []
    
    if branch_id:
        degrees = Degree.objects.filter(branch_id=branch_id).order_by('name')
    
    if degree_id:
        max_year = AcademicYear.objects.filter(degree_id=degree_id).aggregate(models.Max('year'))['year__max']
        if max_year:
            years = range(1, max_year + 1)
            
    context = {'degrees': degrees, 'years': years}
    return render(request, 'admin/orchestrator/partials/_degree_options.html', context)

@staff_member_required
def get_sub_categories_htmx(request):
    master_category_id = request.GET.get('master_category_id')
    sub_categories = FreeContentSubCategory.objects.filter(master_category_id=master_category_id).order_by('name')
    return render(request, 'admin/orchestrator/partials/_category_options_form_row.html', {'sub_categories': sub_categories})

@staff_member_required
def task_log_full_page_view(request, task_id):
    task = get_object_or_404(PendingContentTask, id=task_id)
    # El log se almacena como una lista de diccionarios. Lo invertimos para la vista.
    task_log_reversed = list(reversed(task.task_log))
    
    context = admin.site.each_context(request)
    context.update({
        "title": f"Log de Tarea: {task}",
        "task": task,
        "task_log_reversed": task_log_reversed,
    })
    return render(request, "admin/orchestrator/task_log_full_page.html", context)

@staff_member_required
@require_http_methods(["GET", "POST"])
def create_academic_task_view(request):
    context = admin.site.each_context(request)
    
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        subject = get_object_or_404(Subject, pk=subject_id)
        
        if subject.is_content_generation_locked():
             messages.error(request, f"Ya existe contenido o una tarea activa para la familia de contenido de '{subject.name}'.")
             return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('orchestrator:task_dashboard')))

        try:
            PendingContentTask.objects.create(
                subject=subject,
                assigned_to=request.user,
                task_origin=PendingContentTask.TaskOrigin.MANUAL_CREATION
            )
            messages.success(request, f"Tarea de generación de contenido para '{subject.name}' creada exitosamente.")
        except IntegrityError:
            messages.warning(request, f"Ya existe una tarea activa para '{subject.name}'.")
        
        return HttpResponseRedirect(reverse('orchestrator:task_dashboard'))

    # Lógica GET para el explorador
    university_id = request.GET.get('university_id')
    branch_id = request.GET.get('branch_id')
    degree_id = request.GET.get('degree_id')
    page_number = request.GET.get('page', 1)

    queryset = University.objects.all()
    item_type = 'university'
    breadcrumbs = [{"name": "Universidades", "url": reverse("orchestrator:create_academic_task")}]
    parent_url = None

    if degree_id:
        degree = get_object_or_404(Degree.objects.select_related('branch__university'), pk=degree_id)
        subjects_by_year = defaultdict(list)
        # [CORRECCIÓN] Se anota 'is_locked' para que la plantilla pueda usarlo.
        for subject in Subject.objects.filter(academic_year__degree=degree).select_related('academic_year').order_by('academic_year__year', 'semester', 'name'):
            subject.is_locked = subject.is_content_generation_locked()
            subjects_by_year[subject.academic_year.year].append(subject)
        
        context['subjects_grouped_by_year'] = dict(subjects_by_year)
        item_type = 'subject'
        parent_url = f"?branch_id={degree.branch.id}"
        breadcrumbs.extend([
            {"name": degree.branch.university.name, "url": f"?university_id={degree.branch.university.id}"},
            {"name": degree.branch.name, "url": f"?branch_id={degree.branch.id}"},
            {"name": degree.name}
        ])
    elif branch_id:
        branch = get_object_or_404(Branch.objects.select_related('university'), pk=branch_id)
        queryset = branch.degrees.all()
        item_type = 'degree'
        parent_url = f"?university_id={branch.university.id}"
        breadcrumbs.extend([
            {"name": branch.university.name, "url": f"?university_id={branch.university.id}"},
            {"name": branch.name}
        ])
    elif university_id:
        university = get_object_or_404(University, pk=university_id)
        queryset = university.branches.all()
        item_type = 'branch'
        parent_url = reverse("orchestrator:create_academic_task")
        breadcrumbs.append({"name": university.name})

    paginator = Paginator(queryset, 25)
    page_obj = paginator.get_page(page_number)

    context.update({
        "title": "Explorador y Creación de Tareas Académicas",
        "page_obj": page_obj,
        "item_type": item_type,
        "breadcrumbs": breadcrumbs,
        "parent_url": parent_url,
    })
    return render(request, "admin/orchestrator/create_academic_task.html", context)

@staff_member_required
def create_free_task_view(request):
    context = admin.site.each_context(request)
    if request.method == 'POST':
        form = FreeCourseCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                # 1. Crear el material de contenido primero
                content_material = ContentMaterial.objects.create(
                    title=data['course_title'],
                    author=request.user,
                    is_free_content=True,
                    is_public=False, # Se hará público al completar la tarea
                    master_category=data['master_category'],
                    sub_category=data.get('sub_category')
                )
                # 2. Crear la tarea y vincularla
                PendingContentTask.objects.create(
                    course_title=data['course_title'],
                    prompt_text=data['prompt_text'],
                    assigned_to=request.user,
                    task_origin=PendingContentTask.TaskOrigin.MANUAL_CREATION,
                    content_material=content_material
                )
                messages.success(request, f"Tarea para el curso libre '{data['course_title']}' creada con éxito.")
                return HttpResponseRedirect(reverse('orchestrator:task_dashboard'))
            except IntegrityError:
                messages.error(request, "Ya existe una tarea activa con este título. Por favor, elige otro.")
            except Exception as e:
                messages.error(request, f"Error inesperado al crear la tarea: {e}")
    else:
        form = FreeCourseCreationForm()

    context.update({
        'title': 'Crear Tarea para Curso Libre',
        'form': form,
    })
    return render(request, 'admin/orchestrator/create_free_task.html', context)

@staff_member_required
@require_POST
def set_seed_filters_view(request):
    settings_instance = AutomationSettings.load()
    form = SeedFiltersForm(request.POST, instance=settings_instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Filtros de semilla actualizados.")
    else:
        messages.error(request, "Error al actualizar los filtros.")
    return HttpResponseRedirect(reverse('orchestrator:automation_control_center'))

@staff_member_required
@require_POST
def toggle_automation_status_view(request):
    settings_instance = AutomationSettings.load()
    settings_instance.is_running = not settings_instance.is_running
    settings_instance.save(update_fields=['is_running'])
    
    context = {"settings": settings_instance}
    return render(request, "admin/orchestrator/_automation_status_panel.html", context)

@staff_member_required
@require_POST
def set_active_api_key_view(request):
    key_id = request.POST.get('api_key_id')
    settings_instance = AutomationSettings.load()
    if key_id:
        try:
            key = ApiKey.objects.get(pk=key_id, is_enabled=True, is_quarantined=False)
            settings_instance.active_api_key = key
            settings_instance.save(update_fields=['active_api_key'])
        except ApiKey.DoesNotExist:
            pass # No hacer nada si la clave no es válida
    
    api_keys = ApiKey.objects.all()
    context = {"settings": settings_instance, "api_keys": api_keys}
    return render(request, "admin/orchestrator/_api_key_selector.html", context)

@staff_member_required
@require_POST
def pause_task_view(request, task_id):
    task = get_object_or_404(PendingContentTask, id=task_id)
    if task.status == PendingContentTask.StatusChoices.PROCESSING:
        task.status = PendingContentTask.StatusChoices.PAUSED
        task.save(update_fields=['status'])
    return render(request, 'admin/orchestrator/_task_row.html', {'task': task})

@staff_member_required
@require_POST
def resume_task_view(request, task_id):
    task = get_object_or_404(PendingContentTask, id=task_id)
    if task.status == PendingContentTask.StatusChoices.PAUSED:
        task.status = PendingContentTask.StatusChoices.PENDING # Vuelve a pendiente para ser recogida por el worker
        task.save(update_fields=['status'])
    return render(request, 'admin/orchestrator/_task_row.html', {'task': task})

@staff_member_required
@require_POST
def cancel_task_view(request, task_id):
    task = get_object_or_404(PendingContentTask, id=task_id)
    task.status = PendingContentTask.StatusChoices.FAILED # FAILED es el estado para cancelaciones manuales
    task.save(update_fields=['status'])
    return render(request, 'admin/orchestrator/_task_row.html', {'task': task})

@staff_member_required
def task_row_partial_view(request, task_id):
    task = get_object_or_404(PendingContentTask, id=task_id)
    return render(request, 'admin/orchestrator/_task_row.html', {'task': task})

@staff_member_required
def get_modal_log_content_view(request, task_id):
    task = get_object_or_404(PendingContentTask, id=task_id)
    task_log_reversed = list(reversed(task.task_log))
    return render(request, "admin/orchestrator/_task_log_modal_content.html", {"task": task, "task_log_reversed": task_log_reversed})

@staff_member_required
@require_http_methods(["GET", "POST"])
def reject_free_request_view(request, request_id):
    free_request = get_object_or_404(FreeContentRequest, id=request_id, status=FreeContentRequest.STATUS_PENDING)
    context = admin.site.each_context(request)
    
    if request.method == 'POST':
        form = RejectionReasonForm(request.POST)
        if form.is_valid():
            free_request.status = FreeContentRequest.STATUS_REJECTED
            free_request.rejection_reason = form.cleaned_data['rejection_reason']
            free_request.save()
            messages.success(request, f"La solicitud '{free_request.title}' ha sido rechazada.")
            # TODO: Enviar notificación al usuario
            return HttpResponseRedirect(reverse('orchestrator:task_dashboard'))
    else:
        form = RejectionReasonForm()

    context.update({
        "title": "Rechazar Solicitud de Contenido Libre",
        "free_request": free_request,
        "form": form,
        "breadcrumbs": [
            {"name": "Centro de Control", "url": reverse("orchestrator:task_dashboard")},
            {"name": "Rechazar Solicitud"}
        ]
    })
    return render(request, "admin/orchestrator/reject_request_form.html", context)

@staff_member_required
@require_http_methods(["GET", "POST"])
def delete_free_request_view(request, request_id):
    free_request = get_object_or_404(FreeContentRequest, id=request_id)
    context = admin.site.each_context(request)
    
    if request.method == 'POST':
        title = free_request.title
        free_request.delete()
        messages.success(request, f"La solicitud '{title}' ha sido eliminada permanentemente.")
        return HttpResponseRedirect(reverse('orchestrator:task_dashboard'))

    context.update({
        "title": "Confirmar Eliminación de Solicitud",
        "free_request": free_request,
        "breadcrumbs": [
            {"name": "Centro de Control", "url": reverse("orchestrator:task_dashboard")},
            {"name": "Eliminar Solicitud"}
        ]
    })
    return render(request, "admin/orchestrator/confirm_request_deletion.html", context)

@staff_member_required
def manage_logs_view(request):
    context = admin.site.each_context(request)
    if request.method == 'POST':
        logs_to_delete = request.POST.getlist('logs_to_delete')
        deleted_count = 0
        for log_name in logs_to_delete:
            file_path = os.path.join(LOG_DIRECTORY, log_name)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except OSError as e:
                    messages.error(request, f"No se pudo eliminar {log_name}: {e}")
        if deleted_count > 0:
            messages.success(request, f"{deleted_count} archivo(s) de log eliminado(s) correctamente.")
        return HttpResponseRedirect(reverse('orchestrator:manage_logs'))

    log_files_data = []
    if os.path.exists(LOG_DIRECTORY):
        for filename in os.listdir(LOG_DIRECTORY):
            if filename.endswith('.log'):
                file_path = os.path.join(LOG_DIRECTORY, filename)
                try:
                    stat = os.stat(file_path)
                    log_files_data.append({
                        'name': filename,
                        'size_kb': round(stat.st_size / 1024, 2),
                        'modified_date': datetime.fromtimestamp(stat.st_mtime)
                    })
                except FileNotFoundError:
                    continue # El archivo fue borrado entre el listado y el stat
    
    log_files_data.sort(key=lambda x: x['modified_date'], reverse=True)
    
    context.update({
        'title': 'Gestión de Archivos de Log',
        'log_files': log_files_data
    })
    return render(request, 'admin/orchestrator/manage_logs.html', context)

@staff_member_required
@require_http_methods(["GET", "POST"])
def revise_and_regenerate_view(request, task_id):
    task = get_object_or_404(PendingContentTask, id=task_id, status__in=[
        PendingContentTask.StatusChoices.FAILED, 
        PendingContentTask.StatusChoices.FAILED_FATAL
    ])
    context = admin.site.each_context(request)
    
    if request.method == 'POST':
        form = ReviseTaskForm(request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save(commit=False)
            updated_task.status = PendingContentTask.StatusChoices.PENDING
            updated_task.last_error = None # Limpiar el error anterior
            updated_task.task_log.append({
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "message": f"Tarea revisada y re-encolada por {request.user.username}.",
                "payload": form.cleaned_data
            })
            updated_task.save()
            messages.success(request, f"La tarea para '{task}' ha sido actualizada y puesta en cola para regeneración.")
            return HttpResponseRedirect(reverse('orchestrator:task_dashboard'))
    else:
        form = ReviseTaskForm(instance=task)

    context.update({
        'title': f"Revisar y Regenerar Tarea: {task}",
        'form': form,
        'task': task
    })
    return render(request, 'admin/orchestrator/revise_task_form.html', context)
