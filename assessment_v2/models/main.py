# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/models/main.py
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Exam(models.Model):
    """
    Model for the exam technical header.
    Modelo para la cabecera técnica del examen. Cumple V06DOC_TEMPLATES (Header).
    """
    STATUS_CHOICES = [
        ('PENDING', _('Pendiente')),
        ('GENERATING', _('Generando')),
        ('READY', _('Listo')),
        ('IN_PROGRESS', _('En Progreso')),
        ('COMPLETED', _('Completado')),
        ('GRADING', _('Corrigiendo')),
        ('GRADED', _('Calificado')),
        ('ERROR', _('Error')),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exams_v2')
    content_copy = models.ForeignKey('contents.ContentCopy', on_delete=models.CASCADE, related_name='exams', null=True)

    # Metadatos Académicos (Deducidos por Logic Mapping)
    archetype_id = models.CharField(_('ID Arquetipo'), max_length=50)
    sub_archetype_id = models.CharField(_('ID Sub-Arquetipo'), max_length=50)
    itinerary_id = models.CharField(_('ID Itinerario'), max_length=50)
    pedagogical_level = models.CharField(_('Nivel Pedagógico'), max_length=20)
    immersion_mode = models.CharField(_('Modo de Inmersión'), max_length=20, default='VEHICULAR')
    
    # Configuración de Rigor (V06DOC_LEVELS)
    grading_params = models.JSONField(_('Parámetros de Rigor'), default=dict)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', db_index=True)
    
    # Trazabilidad y Logs
    event_log = models.JSONField(_('Log de Eventos'), default=list, blank=True)
    error_log = models.TextField(_('Log de Error'), blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Examen (V2)')
        verbose_name_plural = _('Exámenes (V2)')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.archetype_id} - {self.pedagogical_level} ({self.uuid})"

class ExamSection(models.Model):
    """
    Represents an exam phase (subdivision).
    Representa una fase o subdivisión del examen. Cumple V06DOC_SUBDIVISIONS.
    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='sections')
    subdivision_id = models.CharField(max_length=50) # SD_READ, SD_LIST...
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    time_limit = models.PositiveIntegerField(default=0, help_text=_("Límite en segundos."))

    class Meta:
        ordering = ['order']

class ExamItem(models.Model):
    """
    Atomic evaluation block.
    Bloque de evaluación atómico. Cumple V06DOC_BLOCKS y V06DOC_TEMPLATES (Item).
    """
    section = models.ForeignKey(ExamSection, on_delete=models.CASCADE, related_name='items')
    block_type = models.CharField(max_length=50) # PRM-STRIKE, CLO-MULTI...
    widget_id = models.CharField(max_length=50) # W-OBJ-STRIKE...
    
    # Contrato JSON segregado
    content = models.JSONField(_('Contenido del Ítem'))
    grading_logic = models.JSONField(_('Lógica de Calificación'))
    metadata = models.JSONField(_('Metadatos Pedagógicos')) # Tags de competencia/cognitivos

    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

class Submission(models.Model):
    """
    Exam delivery and grading report.
    Entrega del examen e informe de calificación. Cumple V06DOC_TEMPLATES (Report).
    """
    exam = models.OneToOneField(Exam, on_delete=models.CASCADE, related_name='submission')
    student_responses = models.JSONField(_('Respuestas del Estudiante'), null=True)
    grading_report = models.JSONField(_('Informe de Calificación'), null=True)
    final_score = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    passed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Entrega de Examen')
        verbose_name_plural = _('Entregas de Exámenes')
