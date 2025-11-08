"""
Admin panel configuration for the Announcement application models.
"""
from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    Customization of the administration interface for the Announcement model.
    """

    list_display = (
        "title",
        "author",
        "created_at",
        "is_recently_published",
    )
    list_filter = ("created_at", "author")
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    @admin.display(boolean=True, description="¿Publicado Recientemente?")
    def is_recently_published(self, obj):
        """
        Indicates if the announcement was published within the last day.
        """
        from django.utils import timezone
        import datetime

        return obj.created_at >= (timezone.now() - datetime.timedelta(days=1))
