from django.contrib import admin
from .models import ShortMessage, UserLink


@admin.register(ShortMessage)
class ShortMessageAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "short_content",
        "is_public",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_public", "created_at", "user")
    search_fields = ("content", "user__username")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25

    fieldsets = (
        (None, {"fields": ("user", "content", "is_public")}),
        (
            "Fechas",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    short_content.short_description = "Contenido (extracto)"


@admin.register(UserLink)
class UserLinkAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "url", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("title", "url", "user__username")
    readonly_fields = ("created_at",)
    list_per_page = 25

    fieldsets = (
        (None, {"fields": ("user", "title", "url")}),
        (
            "Información Adicional",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )
