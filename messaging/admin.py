# /home/MiguelAeTxio/CampuStudiOnline/messaging/admin.py
from django.contrib import admin
from .models import (
    DirectChatSession,
    DirectMessage,
    Browser,
    PushEndpoint,
    UserSubscription,
    SharedContent,
)


@admin.register(SharedContent)
class SharedContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_snapshot', 'shared_by', 'shared_at')
    search_fields = ('title_snapshot', 'shared_by__username')
    list_filter = ('shared_at',)
    readonly_fields = ('shared_by', 'shared_at', 'content_object')


@admin.register(DirectChatSession)
class DirectChatSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user1", "user2", "created_at", "updated_at")
    search_fields = ("user1__username", "user2__username")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user1", "user2")


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "session_display",
        "sender_display",
        "content_preview",
        "timestamp",
        "is_read",
        "read_at",
    )
    search_fields = (
        "sender__username",
        "content",
        "session__user1__username",
        "session__user2__username",
    )
    list_filter = ("timestamp", "is_read", "sender")
    readonly_fields = ("timestamp", "read_at")
    list_editable = ("is_read",)

    def session_display(self, obj):
        return str(obj.session)

    session_display.short_description = "Sesión de Chat"
    session_display.admin_order_field = "session"

    def sender_display(self, obj):
        return obj.sender.username

    sender_display.short_description = "Remitente"
    sender_display.admin_order_field = "sender__username"

    def content_preview(self, obj):
        content_str = str(obj.content)
        return (content_str[:50] + "...") if len(content_str) > 50 else content_str

    content_preview.short_description = "Contenido (Vista Previa)"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("session", "sender", "session__user1", "session__user2")
        )


# =================================================================
# REGISTRATION OF "FORT KNOX" ARCHITECTURE MODELS
# =================================================================


@admin.register(Browser)
class BrowserAdmin(admin.ModelAdmin):
    list_display = ("uuid", "user_agent", "created_at")
    search_fields = ("uuid", "user_agent")
    list_filter = ("created_at",)
    readonly_fields = ("uuid", "user_agent", "created_at")


@admin.register(PushEndpoint)
class PushEndpointAdmin(admin.ModelAdmin):
    list_display = ("browser", "endpoint_snippet", "created_at")
    search_fields = ("browser__uuid", "endpoint")
    list_filter = ("created_at",)
    readonly_fields = ("browser", "endpoint", "keys", "created_at")

    def endpoint_snippet(self, obj):
        return obj.endpoint[:75] + "..." if len(obj.endpoint) > 75 else obj.endpoint

    endpoint_snippet.short_description = "Endpoint (Fragmento)"


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "browser", "device_name", "is_active", "created_at")
    search_fields = ("user__username", "browser__uuid", "device_name")
    list_filter = ("is_active", "created_at")
    list_editable = ("is_active",)
    readonly_fields = ("user", "browser", "created_at")
