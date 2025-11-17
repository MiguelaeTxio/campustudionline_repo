# /home/MiguelAeTxio/CampuStudiOnline/content_automation/admin.py
# El namespace de la app es 'content_automation'

import json
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, include, reverse
from django.utils.html import format_html
from .models import PendingContentTask, ContentRequest, FreeContentRequest
from orchestrator.tasks import generate_full_course_task
from .forms import RejectionReasonForm


@admin.register(ContentRequest)
class ContentRequestAdmin(admin.ModelAdmin):
    """
    Panel de administración para gestionar las solicitudes de contenido de los usuarios.
    """
    list_display = (
        'subject',
        'status',
        'get_request_count',
        'created_at',
        'updated_at',
    )
    list_filter = ('status',)
    search_fields = ('subject__name',)
    ordering = ('-created_at',)
    
    actions = ['accept_requests_and_create_tasks']

    @admin.display(description="Nº de Peticiones", ordering='requesters__count')
    def get_request_count(self, obj):
        return obj.request_count

    @admin.action(description="Aceptar Solicitudes y Crear Tareas de Generación")
    def accept_requests_and_create_tasks(self, request, queryset):
        
        pending_requests = queryset.filter(status=ContentRequest.StatusChoices.PENDING)
        tasks_created_count = 0
        
        for content_request in pending_requests:
            task = PendingContentTask.objects.create(
                subject=content_request.subject,
                assigned_to=request.user
            )
            generate_full_course_task.delay(str(task.id))
            
            content_request.status = ContentRequest.StatusChoices.IN_PROGRESS
            content_request.save(update_fields=['status'])
            
            tasks_created_count += 1

        if tasks_created_count > 0:
            self.message_user(
                request,
                f"{tasks_created_count} tareas de generación han sido creadas y encoladas con éxito.",
                messages.SUCCESS,
            )
            
        skipped_count = queryset.count() - tasks_created_count
        if skipped_count > 0:
            self.message_user(
                request,
                f"{skipped_count} solicitudes fueron omitidas porque no estaban en estado 'Pendiente'.",
                messages.WARNING,
            )


@admin.register(PendingContentTask)
class PendingContentTaskAdmin(admin.ModelAdmin):
    """
    Panel de administración para monitorizar TODAS las tareas de generación de contenido.
    """
    # --- Integración de URLs personalizadas ---
    def get_urls(self):
        urls = super().get_urls()
        # El namespace se hereda del sitio de admin, por lo que las URLs se resolverán como 'admin:...'
        custom_urls = [
            path('', include('content_automation.admin_urls')),
        ]
        return custom_urls + urls

    # --- Acciones de Administrador ---
    actions = ["reset_tasks_to_pending"]

    # --- Configuración de la vista de lista (changelist) ---
    list_display = (
        "get_task_title",
        "status",
        "assigned_to",
        "created_at",
        "updated_at",
        "subject_link",
    )
    list_filter = ("status", "assigned_to")
    list_editable = ("status",)
    search_fields = (
        "subject__name",
        "course_title",
        "prompt_text",
        "assigned_to__username",
    )
    ordering = ("-created_at",)

    # --- Configuración del formulario de detalle (changeform) ---
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "content_material_link",
        "display_task_log",
        "display_structured_content",
    )
    fieldsets = (
        (None, {"fields": ("id", "status", "assigned_to")}),
        ("Detalles de Tarea", {"fields": ("course_title", "prompt_text", "subject")}),
        (
            "Resultados y Depuración",
            {
                "fields": (
                    "content_material_link",
                    "display_structured_content",
                    "notes",
                    "display_task_log",
                ),
            },
        ),
        ("Fechas", {"fields": ("created_at", "updated_at")}),
    )

    def get_task_title(self, obj):
        return (
            obj.course_title
            if obj.course_title
            else (obj.subject.name if obj.subject else "N/A")
        )

    get_task_title.short_description = "Título de la Tarea"

    def subject_link(self, obj):
        if obj.subject:
            url = reverse(
                "admin:academic_structure_subject_change", args=[obj.subject.pk]
            )
            return format_html('<a href="{}">{}</a>', url, obj.subject)
        return "-"

    subject_link.short_description = "Asignatura Académica"

    def content_material_link(self, obj):
        if obj.content_material:
            url = reverse(
                "admin:contents_contentmaterial_change",
                args=[obj.content_material.pk],
            )
            return format_html(
                '<a href="{}">Ver Contenido Generado (ID: {})</a>',
                url,
                obj.content_material.pk,
            )
        return "No generado"

    content_material_link.short_description = "Material de Contenido"

    @admin.display(description="Log de Tarea (JSON)")
    def display_task_log(self, obj):
        if obj.task_log:
            sorted_log = sorted(obj.task_log, key=lambda x: x.get('timestamp', ''), reverse=True)
            pretty_json = json.dumps(sorted_log, indent=2, ensure_ascii=False)
            return format_html("<pre><code>{}</code></pre>", pretty_json)
        return "Log vacío."
        
    @admin.display(description="Contenido Estructurado (JSON)")
    def display_structured_content(self, obj):
        if obj.structured_content:
            pretty_json = json.dumps(obj.structured_content, indent=2, ensure_ascii=False)
            return format_html("<pre><code>{}</code></pre>", pretty_json)
        return "Sin contenido estructurado."

    @admin.action(description="Resetear tareas seleccionadas a 'Pendiente'")
    def reset_tasks_to_pending(self, request, queryset):
        updated_count = queryset.update(status=PendingContentTask.StatusChoices.PENDING)
        self.message_user(
            request,
            f"{updated_count} tareas han sido reseteadas y volverán a ser procesadas.",
            messages.SUCCESS,
        )


@admin.register(FreeContentRequest)
class FreeContentRequestAdmin(admin.ModelAdmin):
    """
    Panel de administración para gestionar las solicitudes de contenido libre.
    """
    list_display = (
        'title',
        'requester',
        'status',
        'created_at',
        'request_actions',
    )
    list_filter = ('status',)
    search_fields = ('title', 'requester__username')
    ordering = ('-created_at',)
    readonly_fields = ('requester', 'created_at', 'updated_at')
    
    actions = ['approve_requests', 'reject_requests', 'resend_feedback_email']

    @admin.display(description="Acciones")
    def request_actions(self, obj):
        if obj.status == FreeContentRequest.STATUS_PENDING:
            # Modificación: pasar los campos de jerarquía al URL
            approve_url = reverse("admin:content_automation_pendingcontenttask_create_free_task") + f"?request_id={obj.pk}"
            
            # Asegurarse de que los campos de jerarquía se incluyan si existen
            if obj.target_discipline:
                approve_url += f"&target_discipline={obj.target_discipline.pk}"
            if obj.target_category:
                approve_url += f"&target_category={obj.target_category.pk}"

            reject_url = reverse("admin:content_automation_pendingcontenttask_reject_free_request", args=[obj.pk])
            
            buttons = f'''
                <div style="display: flex; flex-direction: column; gap: 5px;">
                    <a href="{approve_url}" class="button" style="background-color: #4CAF50; color: white; width: 100px; text-align: center;">Aprobar</a>
                    <a href="{reject_url}" class="button" style="background-color: #f44336; color: white; width: 100px; text-align: center;">Rechazar</a>
                </div>
            '''
            return format_html(buttons)
        return "N/A (Gestionada)"

    # --- Acciones de Administrador (en lote) ---

    @admin.action(description="Aprobar solicitudes y crear tareas (en lote)")
    def approve_requests(self, request, queryset):
        pending_requests = queryset.filter(status=FreeContentRequest.STATUS_PENDING)
        tasks_created_count = 0
        
        for free_request in pending_requests:
            # Recuperar los campos de jerarquía si están disponibles en la solicitud
            target_discipline_id = request.POST.get('target_discipline')
            target_category_id = request.POST.get('target_category')

            task_data = {
                "course_title": free_request.title,
                "prompt_text": free_request.detailed_prompt,
                "assigned_to": request.user,
                "task_origin": PendingContentTask.TaskOrigin.MANUAL_CREATION, # Establecer origen
            }
            
            # Solo añadir campos de jerarquía si están presentes
            if target_discipline_id:
                task_data["target_discipline_id"] = target_discipline_id
            if target_category_id:
                task_data["target_category_id"] = target_category_id

            task = PendingContentTask.objects.create(**task_data)
            
            generate_full_course_task.delay(str(task.id))
            
            free_request.status = FreeContentRequest.STATUS_APPROVED
            free_request.save(update_fields=['status'])
            
            tasks_created_count += 1

        if tasks_created_count > 0:
            self.message_user(
                request,
                f"{tasks_created_count} tareas de contenido libre han sido creadas y encoladas. Se ha notificado a los usuarios.",
                messages.SUCCESS
            )
        
        skipped_count = queryset.count() - tasks_created_count
        if skipped_count > 0:
            self.message_user(
                request,
                f"{skipped_count} solicitudes fueron omitidas porque no estaban en estado 'Pendiente'.",
                messages.WARNING
            )

    @admin.action(description="Rechazar solicitudes seleccionadas (en lote)")
    def reject_requests(self, request, queryset):
        form = RejectionReasonForm(request.POST or None)

        if 'apply' in request.POST and form.is_valid():
            reason = form.cleaned_data['rejection_reason']
            
            pending_requests = queryset.filter(status=FreeContentRequest.STATUS_PENDING)
            updated_count = 0
            
            for free_request in pending_requests:
                free_request.status = FreeContentRequest.STATUS_REJECTED
                free_request.rejection_reason = reason
                free_request.save(update_fields=['status', 'rejection_reason'])
                updated_count += 1

            if updated_count > 0:
                self.message_user(
                    request,
                    f"{updated_count} solicitudes han sido rechazadas. Se ha notificado a los usuarios.",
                    messages.SUCCESS
                )
            
            skipped_count = queryset.count() - updated_count
            if skipped_count > 0:
                self.message_user(
                    request,
                    f"{skipped_count} solicitudes fueron omitidas porque no estaban en estado 'Pendiente'.",
                    messages.WARNING
                )

            return HttpResponseRedirect(request.get_full_path())

        context = {
            'queryset': queryset,
            'form': form,
            'title': u'Seleccionar Motivo del Rechazo',
            'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
        }
        return render(request, 'admin/content_automation/batch_rejection_form.html', context)
        
    @admin.action(description="Reenviar email de feedback al usuario")
    def resend_feedback_email(self, request, queryset):
        eligible_requests = queryset.filter(
            status__in=[FreeContentRequest.STATUS_APPROVED, FreeContentRequest.STATUS_REJECTED]
        )
        resent_count = 0
        for free_request in eligible_requests:
            free_request.save() # Re-guardar dispara la señal post_save
            resent_count += 1
        
        if resent_count > 0:
            self.message_user(
                request,
                f"Se ha reenviado el correo de feedback para {resent_count} solicitudes.",
                messages.SUCCESS
            )
        
        skipped_count = queryset.count() - resent_count
        if skipped_count > 0:
            self.message_user(
                request,
                f"{skipped_count} solicitudes fueron omitidas por no estar en estado 'Aprobada' o 'Rechazada'.",
                messages.WARNING
            )
            
    # --- Lógica de fieldsets dinámicos ---
    
    def get_fieldsets(self, request, obj=None):
        base_fields = (
            (None, {
                'fields': ('title', 'requester', 'status')
            }),
            ('Detalles', {
                'fields': ('detailed_prompt',)
            }),
            ('Fechas', {
                'fields': ('created_at', 'updated_at')
            }),
        )
        if obj and obj.status == FreeContentRequest.STATUS_REJECTED:
            return base_fields + (('Gestión de Rechazo', {
                'fields': ('rejection_reason',),
                'description': 'Por favor, selecciona un motivo para el rechazo.'
            }),)
        return base_fields
