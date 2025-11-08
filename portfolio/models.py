# /home/MiguelAeTxio/CampuStudiOnline/portfolio/models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ShortMessage(models.Model):
    """
    Model for short messages a user can add to their portfolio.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="short_messages",
        verbose_name="Usuario",
    )
    content = models.TextField(
        verbose_name="Contenido del Mensaje",
        help_text=_("Escribe tu mensaje corto aquí (máx. 500 caracteres)."),
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name="¿Mensaje Público?",
        help_text=_(
            "Si no está marcado, solo tú podrás ver este mensaje en tu portafolio."
        ),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Creación"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    def __str__(self):
        return _("Mensaje corto de %(username)s - %(date)s") % {
            "username": self.user.username,
            "date": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }

    class Meta:
        verbose_name = "Mensaje Corto del Portafolio"
        verbose_name_plural = "Mensajes Cortos del Portafolio"
        ordering = ["-created_at"]


class UserLink(models.Model):
    """
    Model for links of interest that a user can add to their portfolio.
    These links are always public.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_links",
        verbose_name="Usuario",
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Título del Enlace",
        help_text=_("Ej: Mi perfil de GitHub, Blog Personal, LinkedIn"),
    )
    url = models.URLField(
        max_length=2000,
        verbose_name="URL del Enlace",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Creación"
    )

    def __str__(self):
        return _("Enlace de %(username)s: %(title)s") % {
            "username": self.user.username,
            "title": self.title,
        }

    class Meta:
        verbose_name = "Enlace de Usuario del Portafolio"
        verbose_name_plural = "Enlaces de Usuario del Portafolio"
        ordering = ["created_at"]
