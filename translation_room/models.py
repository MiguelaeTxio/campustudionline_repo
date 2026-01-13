from django.db import models
from django.conf import settings

class TranslationLog(models.Model):
    """
    Registro de actividad de la Sala de Traducción.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuario")
    source_lang = models.CharField(max_length=100, verbose_name="Idioma Origen")
    target_lang = models.CharField(max_length=100, verbose_name="Idioma Destino")
    char_count = models.IntegerField(verbose_name="Caracteres", help_text="Longitud del texto original")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    is_successful = models.BooleanField(default=True, verbose_name="Éxito")
    error_message = models.TextField(blank=True, null=True, verbose_name="Error Técnico")

    class Meta:
        verbose_name = "Registro de Traducción"
        verbose_name_plural = "Registros de Traducción"
        ordering = ['-timestamp']

    def __str__(self):
        username = self.user.email if self.user else "Anónimo"
        return f"{username} -> {self.char_count} chars ({self.timestamp:%d/%m %H:%M})"
