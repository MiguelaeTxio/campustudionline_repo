# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/models/main.py
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Exam(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_GENERATING = 'GENERATING'
    STATUS_READY = 'READY'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_GRADING = 'GRADING'
    STATUS_GRADED = 'GRADED'
    STATUS_ERROR = 'ERROR'

    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pendiente')),
        (STATUS_GENERATING, _('Generando')),
        (STATUS_READY, _('Listo')),
        (STATUS_IN_PROGRESS, _('En Progreso')),
        (STATUS_COMPLETED, _('Completado')),
        (STATUS_GRADING, _('Corrigiendo')),
        (STATUS_GRADED, _('Calificado')),
        (STATUS_ERROR, _('Error')),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exams_v2', verbose_name=_('Estudiante'))
    
    # Campo recuperado: Vínculo con el material de estudio
    content_copy = models.ForeignKey(
        'contents.ContentCopy', 
        on_delete=models.CASCADE, 
        related_name='exams', 
        null=True, 
        blank=True,
        verbose_name=_('Copia de Estudio')
    )

    archetype_id = models.CharField(_('ID Arquetipo'), max_length=50)
    sub_archetype_id = models.CharField(_('ID Sub-Arquetipo'), max_length=50)
    itinerary_id = models.CharField(_('ID Itinerario'), max_length=50)
    pedagogical_level = models.CharField(_('Nivel Pedagógico'), max_length=20)
    structure = models.JSONField(_('Estructura del Examen'), null=True, blank=True)
    status = models.CharField(_('Estado'), max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    error_log = models.TextField(_('Log de Error'), blank=True, null=True)
    created_at = models.DateTimeField(_('Creado'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Actualizado'), auto_now=True)
    
    class Meta:
        verbose_name = _('Examen (V2)')
        verbose_name_plural = _('Exámenes (V2)')
        ordering = ['-created_at']

    def __str__(self):
        return f"Exam {self.uuid} - {self.archetype_id} ({self.get_status_display()})"

class Submission(models.Model):
    exam = models.OneToOneField(Exam, on_delete=models.CASCADE, related_name='submission', verbose_name=_('Examen'))
    student_responses = models.JSONField(_('Respuestas del Estudiante'), null=True, blank=True)
    grading_report = models.JSONField(_('Informe de Calificación'), null=True, blank=True)
    final_score = models.DecimalField(_('Nota Final'), max_digits=4, decimal_places=2, null=True, blank=True)
    passed = models.BooleanField(_('Aprobado'), default=False)
    submitted_at = models.DateTimeField(_('Entregado'), auto_now_add=True)
    graded_at = models.DateTimeField(_('Calificado'), null=True, blank=True)

    class Meta:
        verbose_name = _('Entrega de Examen')
        verbose_name_plural = _('Entregas de Exámenes')

    def __str__(self):
        return f"Submission for {self.exam.uuid}"
