from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class UniversiaSession(models.Model):
    """
    Representa una sesión de conversación persistente entre un usuario y UniversIA.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='universia_sessions',
        verbose_name=_("Usuario")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de inicio"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Última interacción"))
    is_active = models.BooleanField(default=True, verbose_name=_("Activa"))

    class Meta:
        verbose_name = _("Sesión de UniversIA")
        verbose_name_plural = _("Sesiones de UniversIA")
        ordering = ['-updated_at']

    def __str__(self):
        return f"Sesión de {self.user} ({self.updated_at.strftime('%Y-%m-%d %H:%M')})"

class UniversiaMessage(models.Model):
    """
    Mensaje individual dentro de una sesión de UniversIA.
    """
    ROLE_USER = 'user'
    ROLE_MODEL = 'model' # Mapea a 'model' en la API de Gemini
    
    ROLE_CHOICES = [
        (ROLE_USER, _("Usuario")),
        (ROLE_MODEL, _("UniversIA")),
    ]

    session = models.ForeignKey(
        UniversiaSession,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_("Sesión")
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name=_("Rol"))
    content = models.TextField(verbose_name=_("Contenido"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Marca de tiempo"))
    
    # Metadatos opcionales para contexto (ej: URL donde estaba el usuario)
    context_url = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("URL de Contexto"))

    class Meta:
        verbose_name = _("Mensaje")
        verbose_name_plural = _("Mensajes")
        ordering = ['timestamp']
    
    def __str__(self):
        return f"[{self.role}] {self.content[:30]}..."
