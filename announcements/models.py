# /home/MiguelAeTxio/CampuStudiOnline/announcements/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Announcement(models.Model):
    """
    Represents an announcement published on the board.
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Título del Anuncio",
        help_text=_("Enter a clear and concise title for the announcement."),
    )
    content = models.TextField(
        verbose_name="Contenido del Anuncio",
        help_text=_("Write the full body of your announcement here."),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="published_announcements",
        verbose_name="Autor",
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Creación",
        help_text=_(
            "Date and time the announcement was created (set automatically)."
        ),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Anuncio"
        verbose_name_plural = "Anuncios"
        ordering = ["-created_at"]
