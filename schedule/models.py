from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class AcademicEvent(models.Model):
    class EventType(models.TextChoices):
        CLASS = 'CL', _('Clase')
        EXAM = 'EX', _('Examen')
        PRACTICE = 'PR', _('Práctica')
        TUTORIAL = 'TU', _('Tutoría')
        STUDY_SESSION = 'ST', _('Sesión de Estudio')
        DEADLINE = 'DL', _('Entrega / Deadline')
        PERSONAL = 'PE', _('Personal / Otro')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='academic_events',
        verbose_name=_('Usuario')
    )
    subject = models.ForeignKey(
        'academic_structure.Subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='academic_events',
        verbose_name=_('Asignatura')
    )
    title = models.CharField(_('Título'), max_length=200)
    description = models.TextField(_('Descripción'), blank=True)
    start_time = models.DateTimeField(_('Fecha de inicio'))
    end_time = models.DateTimeField(_('Fecha de fin'))
    event_type = models.CharField(
        _('Tipo de evento'),
        max_length=2,
        choices=EventType.choices,
        default=EventType.PERSONAL
    )
    is_all_day = models.BooleanField(_('Todo el día'), default=False)
    location = models.CharField(_('Ubicación'), max_length=200, blank=True)
    
    reminder_sent = models.BooleanField(_("Recordatorio enviado"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Evento Académico')
        verbose_name_plural = _('Eventos Académicos')
        ordering = ['start_time']

    def clean(self):
        if self.start_time and self.end_time and self.end_time < self.start_time:
            raise ValidationError(_('La fecha de fin no puede ser anterior a la fecha de inicio.'))

    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()})"
