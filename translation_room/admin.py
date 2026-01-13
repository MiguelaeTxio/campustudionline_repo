from django.contrib import admin
from .models import TranslationLog

@admin.register(TranslationLog)
class TranslationLogAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'source_lang', 'target_lang', 'char_count', 'timestamp', 'status_icon')
    list_filter = ('timestamp', 'is_successful', 'target_lang')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'error_message')
    readonly_fields = [field.name for field in TranslationLog._meta.fields]
    
    def user_link(self, obj):
        return obj.user
    user_link.short_description = 'Usuario'
    
    def status_icon(self, obj):
        return "✅" if obj.is_successful else "❌"
    status_icon.short_description = 'Estado'

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
