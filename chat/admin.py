# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/chat/admin.py
from django.contrib import admin
from .models import ChatRoom, RoomMembership, ChatMessage


class RoomMembershipInline(admin.TabularInline):
    model = RoomMembership
    extra = 1
    autocomplete_fields = ["user"]
    fields = ("user", "room", "status", "role", "is_silenced", "date_joined")
    readonly_fields = ("date_joined",)


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_select_related = ("creator", "target_subject", "target_master_category", "target_sub_category")
    list_display = (
        "name",
        "slug",
        "is_private",
        "is_platform_default",
        "creator",
        "created_at",
        "member_count_display",
    )
    list_filter = ("is_private", "is_platform_default", "creator", "created_at")
    search_fields = ("name", "description", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at",)
    autocomplete_fields = ["creator"]

    fieldsets = (
        (None, {"fields": ("name", "slug", "description")}),
        (
            "Configuración de Acceso y Tipo",
            {"fields": ("is_private", "is_platform_default", "creator")},
        ),
        (
            "Información Adicional",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    inlines = [RoomMembershipInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "creator", "target_subject", "target_master_category", "target_sub_category"
        ).prefetch_related(
            "memberships"
        ).defer(
            "description"
        )

    def member_count_display(self, obj):
        # [OPTIMIZACIÓN] Se usa len() con all() para aprovechar el prefetch_related y evitar N+1 queries
        return len(obj.memberships.all())

    member_count_display.short_description = "Nº de Entradas de Membresía"


@admin.register(RoomMembership)
class RoomMembershipAdmin(admin.ModelAdmin):
    list_select_related = ("user", "room")
    list_display = ("user", "room", "status", "role", "is_silenced", "date_joined")
    list_filter = ("room", "status", "role", "is_silenced", "date_joined")
    search_fields = ("user__username", "room__name")
    autocomplete_fields = ["user", "room"]
    readonly_fields = ("date_joined",)
    list_editable = ("status", "role", "is_silenced")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_select_related = ("room", "sender")
    list_display = ("room", "sender_username_display", "get_short_content", "timestamp")
    # [OPTIMIZACIÓN CRÍTICA] Eliminado "room" de list_filter.
    # Cargar miles de salas en el filtro lateral bloqueaba la vista incluso con 0 mensajes.
    list_filter = ("timestamp",) 
    search_fields = ("sender_username_display", "content", "room__name")
    # [OPTIMIZACIÓN] Autocomplete para evitar cargar desplegables gigantes en edición
    autocomplete_fields = ["room", "sender"]
    readonly_fields = (
        "timestamp",
        "sender",
        "sender_username_display",
        "room",
        "content",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "room", "sender"
        ).defer(
            "is_deleted_by_moderator"
        )

    def get_short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    get_short_content.short_description = "Contenido (extracto)"
