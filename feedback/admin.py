from django.contrib import admin
from .models import FeedbackReport

@admin.register(FeedbackReport)
class FeedbackReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'user', 'status', 'created_at')
    list_filter = ('report_type', 'status', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user', 'content_material')
    fieldsets = (
        ('Información del Reporte', {
            'fields': ('user', 'report_type', 'title', 'description')
        }),
        ('Contexto', {
            'fields': ('content_material',)
        }),
        ('Gestión', {
            'fields': ('status', 'admin_response', 'created_at', 'updated_at')
        }),
    )
