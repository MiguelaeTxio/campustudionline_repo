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
    STATUS_CHOICES =[
        ('PENDING', _('Pendiente')),
        ('GENERATING', _('Generando')),
        ('READY', _('Listo')),
        ('IN_PROGRESS', _('En Progreso')),
        ('COMPLETED', _('Completado')),
        ('GRADING', _('Corrigiendo')),
        ('GRADED', _('Calificado')),
        ('ERROR', _('Error')),
        ('EXPIRED_UNTAKEN', _('Caducado (No realizado)')),
    ]

    class Archetype(models.TextChoices):
        ARCH_LANG = 'ARCH_LANG', _('Lenguas Extranjeras')
        ARCH_HEALTH = 'ARCH_HEALTH', _('Ciencias de la Salud')
        ARCH_TECH = 'ARCH_TECH', _('Ciencias Técnicas e Ingeniería')
        ARCH_SOC = 'ARCH_SOC', _('Ciencias Sociales y Jurídicas')
        ARCH_HUM = 'ARCH_HUM', _('Artes y Humanidades')
        ARCH_SCI = 'ARCH_SCI', _('Ciencias Puras y Experimentales')

    class Itinerary(models.TextChoices):
        ITIN_MAI = 'ITIN_MAI', _('Maior / Especialización')
        ITIN_MIN = 'ITIN_MIN', _('Minor / Transversal')
        ITIN_ROT = 'ITIN_ROT', _('Rotatorio Clínico')
        ITIN_PROF = 'ITIN_PROF', _('Profesional / Ingeniería')
        ITIN_INV = 'ITIN_INV', _('Investigador')
        ITIN_DOC = 'ITIN_DOC', _('Docente / Didáctico')

    class PedagogicalLevel(models.TextChoices):
        LVL_A = 'LVL_A', _('Acceso / Fundamentos')
        LVL_B = 'LVL_B', _('Independiente / Aplicación')
        LVL_C = 'LVL_C', _('Maestro / Crítico')

    class ImmersionMode(models.TextChoices):
        VEHICULAR = 'VEHICULAR', _('Idioma Vehicular')
        BILINGUAL = 'BILINGUAL', _('Bilingüe')
        TOTAL = 'TOTAL', _('Inmersión Total')

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exams_v2')
    content_copy = models.ForeignKey('contents.ContentCopy', on_delete=models.CASCADE, related_name='exams', null=True)

    # Metadatos Académicos (Deducidos por Logic Mapping)
    archetype_id = models.CharField(_('ID Arquetipo'), max_length=50, choices=Archetype.choices)
    sub_archetype_id = models.CharField(_('ID Sub-Arquetipo'), max_length=50)
    itinerary_id = models.CharField(_('ID Itinerario'), max_length=50, choices=Itinerary.choices)
    pedagogical_level = models.CharField(_('Nivel Pedagógico'), max_length=20, choices=PedagogicalLevel.choices)
    immersion_mode = models.CharField(_('Modo de Inmersión'), max_length=20, choices=ImmersionMode.choices, default=ImmersionMode.VEHICULAR)
    target_language_code = models.CharField(_('Código de Idioma'), max_length=10, default='es', help_text=_('ISO 639-1 (ej: en, fr, ja)'))
    localized_sections = models.JSONField(_('Secciones Localizadas'), default=dict, blank=True)
    
    # Configuración de Rigor (V06DOC_LEVELS)
    grading_params = models.JSONField(_('Parámetros de Rigor'), default=dict)

    # Anti-Abuso (Regla de las 24 horas)
    expiration_date = models.DateTimeField(_('Fecha de Caducidad'), null=True, blank=True)

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
    class LayoutMode(models.TextChoices):
        STANDARD = 'STANDARD', _('Ancho Completo')
        SPLIT_TEXT = 'SPLIT_TEXT', _('Panel Lateral de Texto')
        SPLIT_VISUAL = 'SPLIT_VISUAL', _('Panel Lateral Visual')

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='sections')
    subdivision_id = models.CharField(max_length=50) # SD_READ, SD_LIST...
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    time_limit = models.PositiveIntegerField(default=0, help_text=_("Límite en segundos."))
    
    #[HITO 06] Soporte para Readings, Casos Clínicos o Gráficos (V06DOC_TEMPLATES)
    section_stimulus = models.TextField(_("Estímulo de Sección"), blank=True, null=True, help_text=_("Texto, HTML o URL base. Usado en lectura (Reading), casos prácticos, o datos compartidos."))
    layout_mode = models.CharField(_("Modo de Layout"), max_length=20, choices=LayoutMode.choices, default=LayoutMode.STANDARD, help_text=_("Define si la sección necesita panel lateral (SPLIT_TEXT, SPLIT_VISUAL) o pantalla completa (STANDARD)."))

    class Meta:
        ordering = ['order']

class ExamItem(models.Model):
    """
    Atomic evaluation block.
    Bloque de evaluación atómico. Cumple V06DOC_BLOCKS y V06DOC_TEMPLATES (Item).
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    section = models.ForeignKey(ExamSection, on_delete=models.CASCADE, related_name='items')
    block_type = models.CharField(max_length=50) # PRM-STRIKE, CLO-MULTI...
    widget_id = models.CharField(max_length=50) # W-OBJ-STRIKE...
    
    # Item Technical Attributes (V06DOC_METADATA)
    # Atributos Técnicos del Ítem (V06DOC_METADATA)
    level_requisite = models.CharField(_('Requisito de Nivel'), max_length=20, default='Mandatory', help_text=_('[Mandatory | Optional | Advanced]'))
    weight = models.DecimalField(_('Peso Relativo'), max_digits=3, decimal_places=2, default=1.00)
    estimated_time = models.PositiveIntegerField(_('Tiempo Estimado (s)'), default=0)
    
    # Contrato JSON segregado
    content = models.JSONField(_('Contenido del Ítem'), default=dict, blank=True)
    grading_logic = models.JSONField(_('Lógica de Calificación'), default=dict, blank=True)
    metadata = models.JSONField(_('Metadatos Pedagógicos'), default=dict, blank=True) # Tags de competencia/cognitivos

    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering =['order']

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

