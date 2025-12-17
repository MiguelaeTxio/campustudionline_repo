from django.contrib import admin
from .models import UniversiaSession, UniversiaMessage

class UniversiaMessageInline(admin.TabularInline):
    model = UniversiaMessage
    extra = 0
    readonly_fields = ('timestamp', 'role', 'context_url')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(UniversiaSession)
class UniversiaSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'user__email')
    inlines = [UniversiaMessageInline]
    readonly_fields = ('created_at', 'updated_at')
