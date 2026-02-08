from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class SubscriptionPlan(models.Model):
    CODE_FREE = 'FREE'
    CODE_PREMIUM = 'PREMIUM'
    CODE_INSTITUTIONAL = 'INSTITUTIONAL'

    PLAN_CHOICES = [
        (CODE_FREE, _('Acceso Gratuito')),
        (CODE_PREMIUM, _('Premium Individual')),
        (CODE_INSTITUTIONAL, _('Licencia Institucional')),
    ]

    name = models.CharField(_('Nombre del Plan'), max_length=50, choices=PLAN_CHOICES, unique=True)
    description = models.TextField(_('Descripción'), blank=True)
    daily_exam_limit = models.PositiveIntegerField(_('Límite Diario de Exámenes'), default=1)
    weekly_exam_limit = models.PositiveIntegerField(_('Límite Semanal de Exámenes'), default=3)
    can_access_c_level = models.BooleanField(_('Acceso a Nivel C (Maestro)'), default=False)
    can_use_specialized_archetypes = models.BooleanField(_('Acceso a Arquetipos Especializados'), default=False)
    monthly_price = models.DecimalField(_('Precio Mensual (€)'), max_digits=6, decimal_places=2, default=0.00)
    is_active = models.BooleanField(_('Activo'), default=True)

    class Meta:
        verbose_name = _('Plan de Suscripción')
        verbose_name_plural = _('Planes de Suscripción')

    def __str__(self):
        return self.get_name_display()

class UserSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessment_subscription', verbose_name=_('Usuario'))
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, verbose_name=_('Plan Actual'))
    start_date = models.DateTimeField(_('Fecha de Inicio'), auto_now_add=True)
    end_date = models.DateTimeField(_('Fecha de Finalización'), null=True, blank=True)
    is_active = models.BooleanField(_('Suscripción Activa'), default=True)
    auto_renew = models.BooleanField(_('Renovación Automática'), default=False)

    class Meta:
        verbose_name = _('Suscripción de Usuario')
        verbose_name_plural = _('Suscripciones de Usuarios')

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
