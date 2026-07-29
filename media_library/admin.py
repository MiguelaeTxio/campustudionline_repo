# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/media_library/admin.py
from django.contrib import admin

from .models import MediaCatalog, MediaLicense, MediaResource


@admin.register(MediaCatalog)
class MediaCatalogAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_enabled", "created_at")
    list_filter = ("is_enabled",)
    search_fields = ("code", "name")


@admin.register(MediaLicense)
class MediaLicenseAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "allows_commercial_use",
        "allows_derivatives",
        "requires_attribution",
        "requires_share_alike",
    )
    list_filter = ("allows_commercial_use", "allows_derivatives")
    search_fields = ("code", "name")


@admin.register(MediaResource)
class MediaResourceAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "catalog",
        "license",
        "status",
        "verified_at",
    )
    list_filter = ("status", "catalog", "license")
    search_fields = ("title", "author", "search_query", "checksum")
    readonly_fields = ("checksum", "created_at", "updated_at")
    list_select_related = ("catalog", "license")
