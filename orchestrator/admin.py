# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/admin.py
import json
import datetime
from django.contrib import admin, messages
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Case, When, Value, TextField
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import path, include, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import ApiKey, AutomationSettings, PendingContentTask, ContentRequest, FreeContentRequest
from .tasks import generate_full_course_task
from .forms import RejectionReasonForm

@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    """
    Interfaz de administración para el modelo ApiKey con indicadores visuales de estado.
    """
    list_display = ('name', 'key_masked', 'status_badge', 'is_enabled', 'is_quarantined')
    list_filter = ('is_enabled', 'is_quarantined')
    search_fields = ('name',)
    ordering = ('name',)
    actions = ['reset_quarantine', 'enable_keys', 'disable_keys']

    def key_masked(self, obj):
        if len(obj.key) > 8:
            return f"{obj.key[:4]}...{obj.key[-4:]}"
        return "********"
    key_masked.short_description = "Clave (Enmascarada)"

    def status_badge(self, obj):
        if obj.is_quarantined:
            color = '#dc3545' # Rojo
            label = 'EN CUARENTENA'
            icon = '&#9888;' # Warning sign
        elif not obj.is_enabled:
            color = '#6c757d' # Gris
            label = 'DESHABILITADA'
            icon = '&#10060;' # Cross
        else:
            color = '#28a745' # Verde
            label = 'ACTIVA'
            icon = '&#10004;' # Check
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px; font-weight: bold;">{} {}</span>',
            color, icon, label
        )
    status_badge.short_description = "Estado Operativo"

    @admin.action(description="Liberar claves de cuarentena")
    def reset_quarantine(self, request, queryset):
        updated = queryset.update(is_quarantined=False)
        self.message_user(request, f"{updated} claves han sido liberadas de la cuarentena.", messages.SUCCESS)

    @admin.action(description="Habilitar claves seleccionadas")
    def enable_keys(self, request, queryset):
        queryset.update(is_enabled=True)

    @admin.action(description="Deshabilitar claves seleccionadas")
    def disable_keys(self, request, queryset):
        queryset.update(is_enabled=False)


@admin.register(AutomationSettings)
class AutomationSettingsAdmin(admin.ModelAdmin):
    """
    Interfaz singleton para la configuración global.
    """
    list_display = ('__str__', 'is_running_badge', 'active_api_key', 'last_run_timestamp', 'quarantine_reset_time')
    readonly_fields = ('event_log', 'last_run_status', 'last_run_timestamp')
    fieldsets = (
        ('Control Maestro', {
            'fields': ('is_running', 'active_api_key')
        }),
        ('Configuración de Semilla (Seed)', {
            'fields': ('seed_branch', 'seed_degree', 'seed_year'),
            'description': 'Punto de partida para la exploración automática de asignaturas.'
        }),
        ('Mantenimiento', {
            'fields': ('quarantine_reset_time', 'last_quarantine_reset_date')
        }),
        ('Parámetros de Resiliencia (Hito 24)', {
            'fields': ('max_task_actuations', 'max_consecutive_api_errors', 'zombie_task_threshold_hours')
        }),
        ('Estado del Sistema', {
            'fields': ('last_run_status', 'last_run_timestamp', 'event_log'),
            'classes': ('collapse',)
        }),
    )

    def is_running_badge(self, obj):
        if obj.is_running:
            return format_html('<span style="color: green; font-weight: bold;">&#9654; EJECUTANDO</span>')
        return format_html('<span style="color: gray; font-weight: bold;">&#9724; DETENIDO</span>')
    is_running_badge.short_description = "Estado del Motor"

    def has_add_permission(self, request):
        # Singleton: solo permitir añadir si no existe ninguno
        return not AutomationSettings.objects.exists()


@admin.register(ContentRequest)
class ContentRequestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status_colored', 'request_count', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject__name',)
    autocomplete_fields = ['subject', 'requesters']
    readonly_fields = ('created_at', 'updated_at')
    
    def status_colored(self, obj):
        colors = {
            'PENDING': 'orange',
            'APPROVED': '#17a2b8',
            'IN_PROGRESS': 'blue',
            'FULFILLED': 'green',
            'REJECTED': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_colored.short_description = "Estado"


@admin.register(FreeContentRequest)
class FreeContentRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'requester', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'requester__username', 'requester__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PendingContentTask)
class PendingContentTaskAdmin(admin.ModelAdmin):
    list_display = ('target_name', 'task_origin', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'task_origin', 'assigned_to')
    search_fields = ('subject__name', 'course_title', 'notes')
    autocomplete_fields = ['subject', 'assigned_to', 'content_material']
    readonly_fields = ('id', 'created_at', 'updated_at', 'task_log', 'structured_content', 'last_error')
    actions = ['download_logs', 'purge_logs']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('id', 'task_origin', 'assigned_to')
        }),
        ('Objetivo', {
            'fields': ('subject', 'course_title', 'prompt_text'),
            'description': 'Especifique Asignatura (para académico) O Título+Prompt (para libre).'
        }),
        ('Estado y Resultados', {
            'fields': ('status', 'content_material', 'api_key_used', 'section_count')
        }),
        ('Logs y Auditoría', {
            'fields': ('notes', 'last_error', 'log_file_path', 'task_log', 'structured_content'),
            'classes': ('collapse',)
        }),
    )

    def target_name(self, obj):
        if obj.subject:
            return f"Asignatura: {obj.subject.name}"
        return f"Libre: {obj.course_title}"
    target_name.short_description = "Objetivo"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include('orchestrator.admin_urls')),
        ]
        return custom_urls + urls

    @admin.action(description="1. Descargar Logs y Contenido (JSON)")
    def download_logs(self, request, queryset):
        """Descarga los campos pesados a un archivo JSON."""
        data = []
        for task in queryset:
            data.append({
                'id': str(task.id),
                'subject': task.subject.name if task.subject else task.course_title,
                'created_at': task.created_at,
                'task_log': task.task_log,
                'structured_content': task.structured_content,
                'notes': task.notes
            })
        
        response = HttpResponse(
            json.dumps(data, cls=DjangoJSONEncoder, indent=2),
            content_type='application/json'
        )
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        response['Content-Disposition'] = f'attachment; filename="tasks_archive_{timestamp}.json"'
        return response

    @admin.action(description="2. Purgar Logs (IRREVERSIBLE - Descargar primero)")
    def purge_logs(self, request, queryset):
        """Reemplaza el contenido pesado con un marcador."""
        archive_marker = {
            "archived": True,
            "date": datetime.date.today().isoformat(),
            "note": "Contenido movido a almacenamiento local por el administrador."
        }
        
        updated_count = queryset.update(
            task_log=archive_marker,
            structured_content=archive_marker,
            notes=Case(
                When(notes="", then=Value("Archivado en local.")),
                default=Concat('notes', Value(' | Archivado en local.')),
                output_field=TextField()
            )
        )
        
        self.message_user(request, f"{updated_count} tareas han sido purgadas y marcadas como archivadas.", messages.WARNING)
