# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/admin.py
from django.contrib import admin
from .models import ApiKey, AutomationSettings

@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    """
    Interfaz de administración para el modelo ApiKey.
    """
    list_display = ('name', 'is_enabled', 'is_quarantined')
    list_filter = ('is_enabled', 'is_quarantined')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(AutomationSettings)
class AutomationSettingsAdmin(admin.ModelAdmin):
    """
    Interfaz de administración para el singleton de AutomationSettings.
    """
    list_display = ('id', 'is_running', 'active_api_key', 'last_run_status', 'last_run_timestamp')
    readonly_fields = ('event_log',)

    def has_add_permission(self, request):
        # Evita que se puedan crear múltiples instancias de la configuración.
        return not AutomationSettings.objects.exists()
