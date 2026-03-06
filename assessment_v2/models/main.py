# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/models/main.py
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Exam(models.Model):
    """
    Model for the exam technical header.
    ---
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
        ('EXPIRED_UNTAKEN', _('Caducado (No realizado)')),
    ]

    class Archetype(models.TextChoices):
        ARCH_LANG = 'ARCH_LANG', _('Lenguas Extranjeras')
        ARCH_HEALTH = 'ARCH_HEALTH', _('Ciencias de la Salud')
        ARCH_TECH = 'ARCH_TECH', _('Ciencias Técnicas e Ingeniería')
        ARCH_SOC = 'ARCH_SOC', _('Ciencias Sociales y Jurídicas')
        ARCH_HUM = 'ARCH_HUM', _('Artes y Humanidades')
        ARCH_SCI = 'ARCH_SCI', _('Ciencias Puras y Experimentales')

    class SubArchetype(models.TextChoices):
        # Arts and Humanities (12)
        SUB_LIN_INSTR = 'SUB-LIN-INSTR', _('Modelo Instrumental')
        SUB_LIN_MINOR = 'SUB-LIN-MINOR', _('Modelo Minor/Iniciación')
        SUB_LIN_PHILO = 'SUB-LIN-PHILO', _('Modelo Filológico')
        SUB_LIN_NORM = 'SUB-LIN-NORM', _('Modelo Norma y Uso')
        SUB_LIN_TRA_TECH = 'SUB-LIN-TRA-TECH', _('Traducción Profesional')
        SUB_LIN_TRA_LIT = 'SUB-LIN-TRA-LIT', _('Traducción Literaria')
        SUB_HUM_HIST = 'SUB-HUM-HIST', _('Modelo Historiográfico')
        SUB_HUM_PHIL = 'SUB-HUM-PHIL', _('Modelo Dialéctico')
        SUB_HUM_ART_HIST = 'SUB-HUM-ART-HIST', _('Modelo Iconográfico')
        SUB_HUM_ART_CREA = 'SUB-HUM-ART-CREA', _('Modelo Bellas Artes')
        SUB_HUM_MUS = 'SUB-HUM-MUS', _('Modelo Musicología')
        SUB_HUM_ANTH = 'SUB-HUM-ANTH', _('Modelo Antropológico')
        # Health Sciences (10)
        SUB_SAN_MED_CLIN = 'SUB-SAN-MED-CLIN', _('Diagnóstico Diferencial y Clínica')
        SUB_SAN_MED_BASIC = 'SUB-SAN-MED-BASIC', _('Básicas Médicas')
        SUB_SAN_ODON = 'SUB-SAN-ODON', _('Odontología')
        SUB_SAN_FISIO = 'SUB-SAN-FISIO', _('Fisioterapia')
        SUB_SAN_CUID = 'SUB-SAN-CUID', _('Enfermería y Cuidados')
        SUB_SAN_LAB = 'SUB-SAN-LAB', _('Bioquímica y Farmacia')
        SUB_SAN_PSY_CLIN = 'SUB-SAN-PSY-CLIN', _('Psicología Clínica')
        SUB_SAN_PSY_EXP = 'SUB-SAN-PSY-EXP', _('Psicología Experimental')
        SUB_SAN_VET = 'SUB-SAN-VET', _('Veterinaria')
        SUB_SAN_NUT = 'SUB-SAN-NUT', _('Nutrición y Dietética')
        # Social and Legal Sciences (10)
        SUB_SOC_LAW_PROC = 'SUB-SOC-LAW-PROC', _('Derecho Procesal')
        SUB_SOC_LAW_DICT = 'SUB-SOC-LAW-DICT', _('Derecho Civil/Penal (Dictamen)')
        SUB_SOC_ECON_QUAN = 'SUB-SOC-ECON_QUAN', _('Economía Cuantitativa')
        SUB_SOC_ECON_MGMT = 'SUB-SOC-ECON_MGMT', _('Organización de Empresas')
        SUB_SOC_EDU_KIDS = 'SUB-SOC-EDU-KIDS', _('Magisterio (Infantil/Primaria)')
        SUB_SOC_EDU_SEC = 'SUB-SOC-EDU-SEC', _('Profesorado (Secundaria)')
        SUB_SOC_COMM_JOUR = 'SUB-SOC-COMM-JOUR', _('Periodismo')
        SUB_SOC_COMM_AV = 'SUB-SOC-COMM-AV', _('Comunicación Audiovisual')
        SUB_SOC_GEOG = 'SUB-SOC-GEOG', _('Geografía')
        SUB_SOC_WORK = 'SUB-SOC-WORK', _('Trabajo Social')
        # Engineering and Architecture (7)
        SUB_TEC_SOFT = 'SUB-TEC-SOFT', _('Ingeniería Informática/Software')
        SUB_TEC_CIVIL = 'SUB-TEC-CIVIL', _('Ingeniería Civil/Caminos')
        SUB_TEC_INDUS = 'SUB-TEC-INDUS', _('Ingeniería Industrial')
        SUB_TEC_CHEM = 'SUB-TEC-CHEM', _('Ingeniería Química')
        SUB_TEC_PROJ = 'SUB-TEC-PROJ', _('Arquitectura (Proyecto)')
        SUB_TEC_CONS = 'SUB-TEC-CONS', _('Edificación y Construcción')
        SUB_TEC_PURE = 'SUB-TEC-PURE', _('Física y Matemáticas Puras')
        # Pure Sciences (6)
        SUB_SCI_BIO = 'SUB-SCI-BIO', _('Biología')
        SUB_SCI_CHEM = 'SUB-SCI-CHEM', _('Química')
        SUB_SCI_PHYS = 'SUB-SCI-PHYS', _('Física Aplicada')
        SUB_SCI_GEOL = 'SUB-SCI-GEOL', _('Geología')
        SUB_SCI_ENV = 'SUB-SCI-ENV', _('Ciencias Ambientales')
        SUB_SCI_DATA = 'SUB-SCI-DATA', _('Ciencia de Datos')

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

    # Academic Metadata (Deduced by Logic Mapping) / Metadatos Académicos (Deducidos por Logic Mapping)
    archetype_id = models.CharField(_('ID Arquetipo'), max_length=50, choices=Archetype.choices)
    sub_archetype_id = models.CharField(_('ID Sub-Arquetipo'), max_length=50, choices=SubArchetype.choices)
    itinerary_id = models.CharField(_('ID Itinerario'), max_length=50, choices=Itinerary.choices)
    pedagogical_level = models.CharField(_('Nivel Pedagógico'), max_length=20, choices=PedagogicalLevel.choices)
    immersion_mode = models.CharField(_('Modo de Inmersión'), max_length=20, choices=ImmersionMode.choices, default=ImmersionMode.VEHICULAR)
    target_language_code = models.CharField(_('Código de Idioma'), max_length=10, default='es', help_text=_('ISO 639-1 (ej: en, fr, ja)'))
    localized_sections = models.JSONField(_('Secciones Localizadas'), default=dict, blank=True)
    
    # Rigor Configuration (V06DOC_LEVELS) / Configuración de Rigor (V06DOC_LEVELS)
    grading_params = models.JSONField(_('Parámetros de Rigor'), default=dict)

    # Anti-Abuse (24h Rule) / Anti-Abuso (Regla de las 24 horas)
    expiration_date = models.DateTimeField(_('Fecha de Caducidad'), null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', db_index=True)
    
    # Traceability and Logs / Trazabilidad y Logs
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
    ---
    Representa una fase o subdivisión del examen. Cumple V06DOC_SUBDIVISIONS.
    """
    class LayoutMode(models.TextChoices):
        STANDARD = 'STANDARD', _('Ancho Completo')
        SPLIT_TEXT = 'SPLIT_TEXT', _('Panel Lateral de Texto')
        SPLIT_VISUAL = 'SPLIT_VISUAL', _('Panel Lateral Visual')

    class Subdivision(models.TextChoices):
        # Communicative Block
        SD_READ = 'SD_READ', _('Comprensión Lectora')
        SD_WRIT = 'SD_WRIT', _('Expresión Escrita')
        SD_LIST = 'SD_LIST', _('Comprensión Auditiva')
        SD_SPEAK = 'SD_SPEAK', _('Expresión Oral')
        SD_MEDI = 'SD_MEDI', _('Mediación')
        # Resolutive Block
        SD_THEO = 'SD_THEO', _('Validación Teórica')
        SD_MODEL = 'SD_MODEL', _('Modelado Formal')
        SD_CALC = 'SD_CALC', _('Precisión Algorítmica')
        SD_VERIF = 'SD_VERIF', _('Verificación Normativa')
        # Assistential / Legal Block
        SD_FACT = 'SD_FACT', _('Extracción de Hechos')
        SD_NORM = 'SD_NORM', _('Encuadre Normativo')
        SD_PROC = 'SD_PROC', _('Derecho Procesal')
        SD_ETHI = 'SD_ETHI', _('Evaluación Deontológica')
        # Critical / Artistic Block
        SD_SOURCE = 'SD_SOURCE', _('Crítica de Fuentes')
        SD_DISC = 'SD_DISC', _('Construcción Discursiva')
        SD_ARTE = 'SD_ARTE', _('Validación Artística')

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='sections')
    subdivision_id = models.CharField(max_length=50, choices=Subdivision.choices) # SD_READ, SD_LIST...
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
    ---
    Bloque de evaluación atómico. Cumple V06DOC_BLOCKS, V06DOC_TEMPLATES y V06DOC_METADATA.
    """
    class Widget(models.TextChoices):
        # Technical (V06DOC_WIDGETS Sec 1)
        W_TECH_CALC = 'W-TECH-CALC', _('Consola de Cálculo Procedimental')
        W_CLIN_SCAN = 'W-CLIN-SCAN', _('Visor de Evidencia Diagnóstica')
        W_OBJ_STRIKE = 'W-OBJ-STRIKE', _('Selector de Respuesta con Riesgo')
        # Discursive & Action (V06DOC_WIDGETS Sec 2)
        W_HUM_TEXT = 'W-HUM-TEXT', _('Editor de Exégesis Crítica')
        W_PROC_ACTION = 'W-PROC-ACTION', _('Panel de Acción Crítica')
        W_COMM_DIALOG = 'W-COMM-DIALOG', _('Interfaz de Mediación Dialéctica')
        W_LAW_NAV = 'W-LAW-NAV', _('Navegador de Marco Normativo')
        # Linguistic & Structural (V06DOC_WIDGETS Sec 3)
        W_TXT_CLOZE = 'W-TXT-CLOZE', _('Integrador de Huecos en Texto')
        W_MIX_MATCH = 'W-MIX-MATCH', _('Matriz de Vinculación')

    class BlockType(models.TextChoices):
        # Objective & Technical
        PRM_STRIKE = 'PRM-STRIKE', _('Respuesta Múltiple (Penalización Progresiva)')
        RBT_CANON = 'RBT-CANON', _('Respuesta Breve (Precisión Terminológica)')
        RPP_TRAZA = 'RPP-TRAZA', _('Resolución Procedimental (Arrastre Error)')
        # Security & Critical Analysis
        CDS_KILL = 'CDS-KILL', _('Checklist Dicotómico Crítico')
        DRA_HOLO = 'DRA-HOLO', _('Disertación (Rúbrica Holística)')
        BMT_SHIFT = 'BMT-SHIFT', _('Mediación y Transferencia de Registro')
        ILC_CONTEXT = 'ILC-CONTEXT', _('Interpretación de Contexto y Datos Brutos')
        EV_PALE = 'EV-PALE', _('Transcripción y Exégesis de Fuentes Primarias')
        # Linguistic & Structural
        CLO_OPEN = 'CLO-OPEN', _('Open Cloze / Rellenado Abierto')
        CLO_MULTI = 'CLO-MULTI', _('Multiple Choice Cloze / Rellenado Selectivo')
        MAT_LINK = 'MAT-LINK', _('Matching / Emparejamiento')

    class LevelRequisite(models.TextChoices):
        # V06DOC_METADATA Sec 3
        MANDATORY = 'MANDATORY', _('Obligatorio')
        OPTIONAL = 'OPTIONAL', _('Opcional')
        ADVANCED = 'ADVANCED', _('Avanzado')

    class FeedbackTaxonomy(models.TextChoices):
        # V06DOC_METADATA Sec 4
        FB_CONCEPT = 'FB_CONCEPT', _('Error Conceptual')
        FB_FORMAL = 'FB_FORMAL', _('Error Formal o de Registro')
        FB_PROCEDURAL = 'FB_PROCEDURAL', _('Error Procedimental o Metodológico')
        FB_SAFETY = 'FB_SAFETY', _('Violación de Seguridad Crítica')

    # [NUEVO] V06DOC_METADATA Sec 1: Competency Domains / Dominios de Competencia
    class CompetencyDomain(models.TextChoices):
        COMP_GEN = 'COMP_GEN', _('Competencias Genéricas')
        COMP_TRA = 'COMP_TRA', _('Competencias Transversales')
        COMP_ESP = 'COMP_ESP', _('Competencias Específicas')
        COMP_PROF = 'COMP_PROF', _('Competencias Profesionales')

    # [NUEVO] V06DOC_METADATA Sec 2: Cognitive Taxonomy / Taxonomía Cognitiva
    class CognitiveTaxonomy(models.TextChoices):
        COG_REM = 'COG_REM', _('Recordar (Identificación)')
        COG_UND = 'COG_UND', _('Comprender (Explicación)')
        COG_APP = 'COG_APP', _('Aplicar (Uso Práctico)')
        COG_ANA = 'COG_ANA', _('Analizar (Relación Lógica)')
        COG_EVAL = 'COG_EVAL', _('Evaluar (Juicio Crítico)')
        COG_CREA = 'COG_CREA', _('Crear (Generación Original)')

    # [NUEVO] V06DOC_METADATA Sec 3: Fail Logic / Lógica de Fallo
    class FailLogic(models.TextChoices):
        PENALTY = 'PENALTY', _('Penalización Estándar')
        FATAL = 'FATAL', _('Error Fatal (Muerte Súbita)')
        PARTIAL = 'PARTIAL', _('Crédito Parcial')

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    section = models.ForeignKey(ExamSection, on_delete=models.CASCADE, related_name='items')
    block_type = models.CharField(max_length=50, choices=BlockType.choices) # PRM-STRIKE, CLO-MULTI...
    widget_id = models.CharField(max_length=50, choices=Widget.choices) # W-OBJ-STRIKE...
    
    # Item Technical Attributes (V06DOC_METADATA) / Atributos Técnicos del Ítem
    level_requisite = models.CharField(_('Requisito de Nivel'), max_length=20, choices=LevelRequisite.choices, default=LevelRequisite.MANDATORY)
    weight = models.DecimalField(_('Peso Relativo'), max_digits=3, decimal_places=2, default=1.00)
    estimated_time = models.PositiveIntegerField(_('Tiempo Estimado (s)'), default=0)
    
    # [NUEVO] V06DOC_METADATA Sec 3: Fail Logic explícito
    fail_logic = models.CharField(_('Lógica de Fallo'), max_length=20, choices=FailLogic.choices, default=FailLogic.PENALTY)
    
    # Segregated JSON Contract / Contrato JSON Segregado
    content = models.JSONField(_('Contenido del Ítem'), default=dict, blank=True)
    grading_logic = models.JSONField(_('Lógica de Calificación'), default=dict, blank=True)
    metadata = models.JSONField(_('Metadatos Pedagógicos'), default=dict, blank=True) # Tags adicionales

    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering =['order']

class Submission(models.Model):
    """
    Exam delivery and grading report.
    ---
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
