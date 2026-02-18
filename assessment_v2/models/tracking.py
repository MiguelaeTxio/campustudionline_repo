# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/models/tracking.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class TokenUsage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='token_usage_logs', verbose_name=_('Usuario'))
    date = models.DateField(_('Fecha'), auto_now_add=True)
    input_tokens_total = models.PositiveIntegerField(_('Tokens de Entrada'), default=0)
    output_tokens_total = models.PositiveIntegerField(_('Tokens de Salida'), default=0)
    estimated_cost_usd = models.DecimalField(_('Coste Estimado (USD)'), max_digits=10, decimal_places=6, default=0.0)

    class Meta:
        verbose_name = _('Uso Diario de Tokens')
        verbose_name_plural = _('Registros de Uso Diario')
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class CostLog(models.Model):
    exam = models.ForeignKey('assessment_v2.Exam', on_delete=models.SET_NULL, null=True, blank=True, related_name='cost_logs', verbose_name=_('Examen Relacionado'))
    operation_type = models.CharField(_('Tipo de Operación'), max_length=50)
    model_name = models.CharField(_('Modelo IA'), max_length=100)
    # [HITO 6] Campo para auditoría de costes por clave API
    api_key_name = models.CharField(_('Clave API'), max_length=100, null=True, blank=True)
    input_tokens = models.PositiveIntegerField(_('Tokens Entrada'))
    output_tokens = models.PositiveIntegerField(_('Tokens Salida'))
    cost_usd = models.DecimalField(_('Coste (USD)'), max_digits=10, decimal_places=6)
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)

    class Meta:
        verbose_name = _('Log de Coste Detallado')
        verbose_name_plural = _('Logs de Coste Detallados')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.operation_type} - {self.cost_usd} USD"
