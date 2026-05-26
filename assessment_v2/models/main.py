# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/models/main.py
"""
Assessment V2 - Core Models.
Defines the relational structure for the AI-powered self-assessment engine (Hito 6).
Complies with V06DOC_TEMPLATES, V06DOC_METADATA, V06DOC_BLOCKS, V06DOC_WIDGETS,
V06DOC_SUBARCHETYPES and V06DOC_SUBDIVISIONS (v5.9 — 2026-05-16).
---
Modelos principales del motor de autoevaluación con IA (Hito 6).
Cumple con V06DOC_TEMPLATES, V06DOC_METADATA, V06DOC_BLOCKS, V06DOC_WIDGETS,
V06DOC_SUBARCHETYPES y V06DOC_SUBDIVISIONS (v5.9 — 2026-05-16).
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Exam(models.Model):
    """
    Root entity representing a single assessment session.
    Stores all academic metadata deduced by the hybrid classification protocol.
    Ref: V06DOC_TEMPLATES (Exam Header), V06DOC_LOGIC_MAPPING, V06DOC_LEVELS.
    ---
    Entidad raíz que representa una sesión de evaluación completa.
    Almacena todos los metadatos académicos deducidos por el protocolo de clasificación híbrido.
    Ref: V06DOC_TEMPLATES (Cabecera de Examen), V06DOC_LOGIC_MAPPING, V06DOC_LEVELS.
    """

    # -------------------------------------------------------------------------
    # Status lifecycle / Ciclo de vida de estados
    # -------------------------------------------------------------------------
    STATUS_CHOICES = [
        ('PENDING',          _('Pendiente')),
        ('GENERATING',       _('Generando')),
        ('READY',            _('Listo para realizar')),
        ('IN_PROGRESS',      _('En Progreso')),
        ('GRADING',          _('Corrigiendo')),
        ('GRADED',           _('Calificado')),
        ('ERROR',            _('Error de Generación')),
        ('EXPIRED_UNTAKEN',  _('Caducado (No realizado)')),
    ]

    # -------------------------------------------------------------------------
    # Archetype taxonomy / Taxonomía de arquetipos
    # Ref: V06DOC_ARCHETYPES
    # -------------------------------------------------------------------------
    class Archetype(models.TextChoices):
        ARCH_LANG   = 'ARCH_LANG',   _('Lenguas Extranjeras (Instrumental/CLM)')
        ARCH_HEALTH = 'ARCH_HEALTH', _('Ciencias de la Salud (ECOE)')
        ARCH_TECH   = 'ARCH_TECH',   _('Ciencias Técnicas e Ingeniería (Resolutivo)')
        ARCH_SOC    = 'ARCH_SOC',    _('Ciencias Sociales y Jurídicas (Casuístico)')
        ARCH_HUM    = 'ARCH_HUM',    _('Artes y Humanidades (Hermenéutico)')
        ARCH_SCI    = 'ARCH_SCI',    _('Ciencias Puras y Experimentales (Metodológico)')

    # -------------------------------------------------------------------------
    # Sub-archetype taxonomy — 87 certified sub-archetypes (v5.9)
    # Taxonomía de subarquetipos — 87 subarquetipos certificados (v5.9)
    # Ref: V06DOC_SUBARCHETYPES
    # -------------------------------------------------------------------------
    class SubArchetype(models.TextChoices):
        # --- RAMA LENGUAS (7) ---
        SUB_LIN_INSTR     = 'SUB-LIN-INSTR',     _('Instrumental / CertAcles CLM-UGR')
        SUB_LIN_MINOR     = 'SUB-LIN-MINOR',     _('Minor / Iniciación (Lengua B/C)')
        SUB_LIN_PHILO     = 'SUB-LIN-PHILO',     _('Filológico / Lingüística Histórica')
        SUB_LIN_ECDO      = 'SUB-LIN-ECDO',      _('Ecdótica / Edición y Crítica Textual')
        SUB_LIN_NORM      = 'SUB-LIN-NORM',      _('Norma y Uso / El Español Actual')
        SUB_LIN_TRA_TECH  = 'SUB-LIN-TRA-TECH',  _('Traducción Especializada B-A Inglés')
        SUB_LIN_TRA_LIT   = 'SUB-LIN-TRA-LIT',   _('Traducción Literaria / Literatura y Traducción')

        # --- RAMA HUMANIDADES (6) ---
        SUB_HUM_HIST      = 'SUB-HUM-HIST',      _('Historiográfico (Historia UGR)')
        SUB_HUM_PHIL      = 'SUB-HUM-PHIL',      _('Dialéctico (Filosofía UGR)')
        SUB_HUM_ART_HIST  = 'SUB-HUM-ART-HIST',  _('Iconográfico (Historia del Arte UGR)')
        SUB_HUM_ART_CREA  = 'SUB-HUM-ART-CREA',  _('Bellas Artes — Emulación Parcial Certificada')
        SUB_HUM_MUS       = 'SUB-HUM-MUS',       _('Musicológico (Historia y Ciencias de la Música UGR)')
        SUB_HUM_ANTH      = 'SUB-HUM-ANTH',      _('Antropológico — Subarquetipo Transversal')

        # --- RAMA CIENCIAS DE LA SALUD (18) ---
        SUB_SAN_MED_CLIN      = 'SUB-SAN-MED-CLIN',      _('Diagnóstico Clínico y Razonamiento (Medicina UGR)')
        SUB_SAN_MED_BASIC     = 'SUB-SAN-MED-BASIC',     _('Ciencias Básicas Médicas: Anatomía e Histología')
        SUB_SAN_MED_FISIO_GEN = 'SUB-SAN-MED-FISIO-GEN', _('Fisiología General y Médica (Medicina UGR)')
        SUB_SAN_MED_FISIO_NEU = 'SUB-SAN-MED-FISIO-NEURO', _('Fisiología Neurológica (Medicina UGR)')
        SUB_SAN_CUID          = 'SUB-SAN-CUID',          _('Cuidados / Enfermería NANDA (UGR)')
        SUB_SAN_ODON          = 'SUB-SAN-ODON',          _('Odontología — Emulación Parcial Certificada')
        SUB_SAN_FISIO         = 'SUB-SAN-FISIO',         _('Fisioterapia — Emulación Parcial Certificada')
        SUB_SAN_BIOQUIM       = 'SUB-SAN-BIOQUIM',       _('Bioquímica Metabólica (Farmacia UGR) — EP Cert.')
        SUB_SAN_FARM          = 'SUB-SAN-FARM',          _('Farmacología I y II (Farmacia UGR)')
        SUB_SAN_PSY_DIAG      = 'SUB-SAN-PSY-DIAG',      _('Psicopatología del Adulto (Psicología UGR)')
        SUB_SAN_PSY_EVAL      = 'SUB-SAN-PSY-EVAL',      _('Evaluación Psicológica: Técnicas y Aplicaciones')
        SUB_SAN_PSY_MET       = 'SUB-SAN-PSY-MET',       _('Métodos y Diseños (Psicología UGR)')
        SUB_SAN_PSY_STAT      = 'SUB-SAN-PSY-STAT',      _('Descripción y Exploración de Datos (Psicología)')
        SUB_SAN_VET_CLIN      = 'SUB-SAN-VET-CLIN',      _('Veterinaria Clínica (UCO) — EP Certificada')
        SUB_SAN_VET_CIR       = 'SUB-SAN-VET-CIR',       _('Cirugía Veterinaria (UCO) — EP Certificada')
        SUB_SAN_NUT_DIET      = 'SUB-SAN-NUT-DIET',      _('Dietética y Nutrición Clínica (UGR)')
        SUB_SAN_NUT_BROM      = 'SUB-SAN-NUT-BROM',      _('Bromatología (Nutrición UGR) — EP Certificada')
        SUB_SAN_NUT_SPUB      = 'SUB-SAN-NUT-SPUB',      _('Salud Pública y Alimentación en Colectividades')

        # --- RAMA CIENCIAS SOCIALES Y JURÍDICAS (26) ---
        SUB_SOC_LAW_PROC_CIV  = 'SUB-SOC-LAW-PROC-CIV',  _('Derecho Procesal Civil (UGR)')
        SUB_SOC_LAW_PROC_PEN  = 'SUB-SOC-LAW-PROC-PEN',  _('Derecho Procesal Penal (UGR)')
        SUB_SOC_LAW_DICT_CIV  = 'SUB-SOC-LAW-DICT-CIV',  _('Derecho Civil I-IV — Dictamen (UGR)')
        SUB_SOC_LAW_DICT_PEN  = 'SUB-SOC-LAW-DICT-PEN',  _('Derecho Penal I-II — Dictamen (UGR)')
        SUB_SOC_ECON_QUAN_STAT = 'SUB-SOC-ECON-QUAN-STAT', _('Estadística y Técnicas Cuantitativas (UGR)')
        SUB_SOC_ECON_QUAN_ECON = 'SUB-SOC-ECON-QUAN-ECON', _('Econometría I-III (Economía UGR)')
        SUB_SOC_ECON_MGMT_ACC  = 'SUB-SOC-ECON-MGMT-ACC',  _('Contabilidad Financiera y de Gestión (UGR)')
        SUB_SOC_ECON_MGMT_STR  = 'SUB-SOC-ECON-MGMT-STR',  _('Dirección Estratégica I-II (ADE UGR)')
        SUB_SOC_ECON_MGMT_ECO  = 'SUB-SOC-ECON-MGMT-ECO',  _('Microeconomía y Macroeconomía (UGR)')
        SUB_SOC_EDU_KIDS       = 'SUB-SOC-EDU-KIDS',        _('Magisterio Infantil/Primaria DUA (UGR)')
        SUB_SOC_EDU_SEC        = 'SUB-SOC-EDU-SEC',         _('Máster Profesorado Secundaria MAES (UGR)')
        SUB_SOC_COMM_JOUR      = 'SUB-SOC-COMM-JOUR',       _('Periodismo y Redacción (UGR)')
        SUB_SOC_COMM_AV        = 'SUB-SOC-COMM-AV',         _('Comunicación Audiovisual y Guion (UGR)')
        SUB_SOC_GEOG_SIG       = 'SUB-SOC-GEOG-SIG',        _('Sistemas de Información Geográfica (UGR)')
        SUB_SOC_GEOG_TER       = 'SUB-SOC-GEOG-TER',        _('Geografía Humana y Territorial (UGR)')
        SUB_SOC_GEOG_FIS       = 'SUB-SOC-GEOG-FIS',        _('Geografía Física y Climatología (UGR)')
        SUB_SOC_WORK_INT       = 'SUB-SOC-WORK-INT',        _('Trabajo Social: Intervención Individual/Familiar')
        SUB_SOC_WORK_POL       = 'SUB-SOC-WORK-POL',        _('Trabajo Social: Política Social y Bienestar')
        SUB_SOC_WORK_MED       = 'SUB-SOC-WORK-MED',        _('Trabajo Social: Mediación y Ámbitos Especializados')

        # --- RAMA INGENIERÍA Y ARQUITECTURA (17) ---
        SUB_TEC_SOFT_ALG   = 'SUB-TEC-SOFT-ALG',   _('Algoritmia y Estructuras de Datos (ETSIIT-UGR)')
        SUB_TEC_SOFT_DS    = 'SUB-TEC-SOFT-DS',    _('Diseño de Software e Ingeniería (ETSIIT-UGR)')
        SUB_TEC_SOFT_SE    = 'SUB-TEC-SOFT-SE',    _('Ingeniería del Software (ETSIIT-UGR)')
        SUB_TEC_CIVIL_STRUCT = 'SUB-TEC-CIVIL-STRUCT', _('Estructuras de Edificación (ETSICCP-UGR)')
        SUB_TEC_CIVIL_CONC   = 'SUB-TEC-CIVIL-CONC',   _('Hormigón Armado y Pretensado (ETSICCP-UGR)')
        SUB_TEC_CIVIL_STEEL  = 'SUB-TEC-CIVIL-STEEL',  _('Estructuras Metálicas (ETSICCP-UGR)')
        SUB_TEC_INDUS_THERMO = 'SUB-TEC-INDUS-THERMO', _('Termodinámica y Motores (EPSC-UCO)')
        SUB_TEC_INDUS_TMM    = 'SUB-TEC-INDUS-TMM',    _('Teoría de Máquinas y Mecanismos (EPSC-UCO)')
        SUB_TEC_INDUS_DEM    = 'SUB-TEC-INDUS-DEM',    _('Diseño y Fabricación — Ingeniería Industrial (UCO)')
        SUB_TEC_CHEM_BAL     = 'SUB-TEC-CHEM-BAL',     _('Balances de Materia y Energía (IQ-UGR)')
        SUB_TEC_CHEM_REACT   = 'SUB-TEC-CHEM-REACT',   _('Ingeniería de Reactores Químicos (IQ-UGR)')
        SUB_TEC_PROJ_ARCH    = 'SUB-TEC-PROJ-ARCH',    _('Proyectos de Arquitectura (ETSAG-UGR)')
        SUB_TEC_PROJ_URB     = 'SUB-TEC-PROJ-URB',     _('Urbanismo y Ordenación del Territorio (ETSAG-UGR)')
        SUB_TEC_CONS_TECH    = 'SUB-TEC-CONS-TECH',    _('Tecnología de la Construcción (ETSIE-UGR)')
        SUB_TEC_CONS_MAN     = 'SUB-TEC-CONS-MAN',     _('Gestión y Economía de la Construcción (ETSIE-UGR)')
        SUB_TEC_PURE_ANAL    = 'SUB-TEC-PURE-ANAL',    _('Análisis Matemático (Grado Matemáticas UGR)')
        SUB_TEC_PURE_ALGSTR  = 'SUB-TEC-PURE-ALGSTR',  _('Álgebra Estructural y Topología (Matemáticas UGR)')

        # --- RAMA CIENCIAS (14) ---
        SUB_SCI_BIO_GEN   = 'SUB-SCI-BIO-GEN',   _('Biología Molecular y Genética (UGR)')
        SUB_SCI_BIO_ZOO   = 'SUB-SCI-BIO-ZOO',   _('Zoología y Botánica (UGR)')
        SUB_SCI_BIO_ECO   = 'SUB-SCI-BIO-ECO',   _('Ecología (UGR)')
        SUB_SCI_CHEM_ORG  = 'SUB-SCI-CHEM-ORG',  _('Química Orgánica Pura (UGR)')
        SUB_SCI_CHEM_INORG = 'SUB-SCI-CHEM-INORG', _('Química Inorgánica Pura (UGR)')
        SUB_SCI_PHYS_EM   = 'SUB-SCI-PHYS-EM',   _('Electromagnetismo (Física UGR)')
        SUB_SCI_PHYS_QM   = 'SUB-SCI-PHYS-QM',   _('Mecánica Cuántica (Física UGR)')
        SUB_SCI_GEOL_MIN  = 'SUB-SCI-GEOL-MIN',  _('Mineralogía y Petrología (UGR)')
        SUB_SCI_GEOL_STRAT = 'SUB-SCI-GEOL-STRAT', _('Estratigrafía (UGR)')
        SUB_SCI_GEOL_MAP  = 'SUB-SCI-GEOL-MAP',  _('Cartografía Geológica (UGR)')
        SUB_SCI_ENV_RES   = 'SUB-SCI-ENV-RES',   _('Gestión de Residuos y Recursos (UGR)')
        SUB_SCI_ENV_CONT  = 'SUB-SCI-ENV-CONT',  _('Contaminación Ambiental (UGR)')
        SUB_SCI_DATA_STAT = 'SUB-SCI-DATA-STAT', _('Estadística Computacional e Inferencia (UCM GIDIA)')
        SUB_SCI_DATA_ML   = 'SUB-SCI-DATA-ML',   _('Aprendizaje Automático e IA (UCM GIDIA)')
        SUB_SCI_DATA_BIG  = 'SUB-SCI-DATA-BIG',  _('Ingeniería de Datos y Big Data (UCM GIDIA)')

    # -------------------------------------------------------------------------
    # Itinerary taxonomy / Taxonomía de itinerarios
    # Ref: V06DOC_SUBDIVISIONS Sección 1
    # -------------------------------------------------------------------------
    class Itinerary(models.TextChoices):
        ITIN_MAI  = 'ITIN_MAI',  _('Maior / Especialización de Grado (Nivel Catedrático)')
        ITIN_MIN  = 'ITIN_MIN',  _('Minor / Mención Transversal (Nivel Competente)')
        ITIN_ROT  = 'ITIN_ROT',  _('Rotatorio Clínico / Seguridad (Dicotómico)')
        ITIN_PROF = 'ITIN_PROF', _('Profesional / Ingeniería (Normativo-Ejecutivo)')
        ITIN_INV  = 'ITIN_INV',  _('Investigador / Académico (Metodológico)')
        ITIN_DOC  = 'ITIN_DOC',  _('Docente / Didáctico (Transpositivo)')

    # -------------------------------------------------------------------------
    # Pedagogical level taxonomy / Taxonomía de niveles pedagógicos
    # Ref: V06DOC_LEVELS Sección 1
    # -------------------------------------------------------------------------
    class PedagogicalLevel(models.TextChoices):
        LVL_A = 'LVL_A', _('Acceso / Fundamentos (A1-A2): Descriptivo')
        LVL_B = 'LVL_B', _('Independiente / Aplicación (B1-B2): Procedimental')
        LVL_C = 'LVL_C', _('Maestro / Crítico (C1-C2): Epistemológico')

    # -------------------------------------------------------------------------
    # Immersion mode taxonomy / Taxonomía de modos de inmersión
    # Ref: V06DOC_LEVELS Sección 4
    # -------------------------------------------------------------------------
    class ImmersionMode(models.TextChoices):
        VEHICULAR = 'VEHICULAR', _('Idioma Vehicular (Castellano)')
        BILINGUAL = 'BILINGUAL', _('Bilingüe (Castellano + Idioma Objetivo)')
        TOTAL     = 'TOTAL',     _('Inmersión Total (Idioma Objetivo Dinámico)')

    # -------------------------------------------------------------------------
    # Fields / Campos
    # -------------------------------------------------------------------------
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exams_v2',
        verbose_name=_('Usuario')
    )
    content_copy = models.ForeignKey(
        'contents.ContentCopy',
        on_delete=models.CASCADE,
        related_name='exams',
        null=True,
        verbose_name=_('Copia de Estudio')
    )

    # Academic metadata / Metadatos académicos
    # Deduced by the hybrid protocol (V06DOC_LOGIC_MAPPING)
    # Deducidos por el protocolo híbrido (V06DOC_LOGIC_MAPPING)
    archetype_id = models.CharField(
        _('ID Arquetipo'), max_length=20, choices=Archetype.choices
    )
    sub_archetype_id = models.CharField(
        _('ID Sub-Arquetipo'), max_length=50, choices=SubArchetype.choices
    )
    itinerary_id = models.CharField(
        _('ID Itinerario'), max_length=20, choices=Itinerary.choices,
        default=Itinerary.ITIN_MIN
    )
    pedagogical_level = models.CharField(
        _('Nivel Pedagógico'), max_length=10, choices=PedagogicalLevel.choices,
        default=PedagogicalLevel.LVL_B
    )
    immersion_mode = models.CharField(
        _('Modo de Inmersión'), max_length=20, choices=ImmersionMode.choices,
        default=ImmersionMode.VEHICULAR
    )
    target_language_code = models.CharField(
        _('Código ISO de Idioma Objetivo'), max_length=10, default='es',
        help_text=_('ISO 639-1 (ej: en, fr, ja, ar). Solo relevante para ARCH_LANG.')
    )
    localized_sections = models.JSONField(
        _('Secciones Localizadas'), default=dict, blank=True,
        help_text=_('Títulos e instrucciones traducidos al idioma objetivo (solo ARCH_LANG).')
    )

    # Rigor configuration / Configuración de rigor
    # Pre-calculated from V06DOC_LEVELS intersection matrix
    # Pre-calculada desde la matriz de intersección V06DOC_LEVELS
    grading_params = models.JSONField(
        _('Parámetros de Rigor'), default=dict,
        help_text=_('Rigor factor y penalty_threshold calculados al crear el examen.')
    )

    # Sequential navigation flag / Flag de navegación secuencial
    # Mandatory for ARCH_LANG (V06DOC_ARCHETYPES: Non-Backtracking)
    # Obligatorio para ARCH_LANG (V06DOC_ARCHETYPES: Navegación Unidireccional Sellada)
    is_sequential = models.BooleanField(
        _('Secuencial Obligatorio'), default=False,
        help_text=_('Si True, impide el retroceso a secciones anteriores (Non-Backtracking).')
    )

    # Anti-abuse: 24h expiration rule / Anti-abuso: regla de caducidad de 24h
    # Ref: V06DOC_TEMPLATES (Sección 1 — Regla de Negocio Anti-Abuso)
    expiration_date = models.DateTimeField(
        _('Fecha de Caducidad'), null=True, blank=True,
        help_text=_('24h tras el estado READY. Penalización total si no se realiza.')
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING', db_index=True,
        verbose_name=_('Estado')
    )

    # Traceability / Trazabilidad
    event_log = models.JSONField(_('Log de Eventos'), default=list, blank=True)
    error_log  = models.TextField(_('Log de Error'), blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name          = _('Examen (V2)')
        verbose_name_plural   = _('Exámenes (V2)')
        ordering              = ['-created_at']
        indexes               = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return f"[{self.archetype_id}] {self.sub_archetype_id} — {self.pedagogical_level} ({str(self.uuid)[:8]})"


class ExamSection(models.Model):
    """
    Represents a single exam phase (subdivision).
    Each section maps to a certified sub-division from V06DOC_SUBDIVISIONS.
    The layout_mode controls the frontend panel distribution per V06DOC_TEMPLATES.
    ---
    Representa una fase o subdivisión del examen.
    Cada sección mapea a una subdivisión certificada de V06DOC_SUBDIVISIONS.
    El layout_mode controla la distribución de paneles en frontend según V06DOC_TEMPLATES.
    """

    # -------------------------------------------------------------------------
    # Layout mode taxonomy / Taxonomía de modos de layout
    # Ref: V06DOC_TEMPLATES Sección 2 (layout_mode)
    # -------------------------------------------------------------------------
    class LayoutMode(models.TextChoices):
        STANDARD     = 'STANDARD',     _('Ancho Completo — Sin panel lateral')
        SPLIT_TEXT   = 'SPLIT_TEXT',   _('Panel Lateral de Texto (Reading/Caso/Corpus)')
        SPLIT_VISUAL = 'SPLIT_VISUAL', _('Panel Lateral Visual (Imagen/Partitura/Obra)')

    # -------------------------------------------------------------------------
    # Subdivision taxonomy — All certified subdivisions (v5.9)
    # Taxonomía de subdivisiones — Todas las subdivisiones certificadas (v5.9)
    # Ref: V06DOC_SUBDIVISIONS
    # -------------------------------------------------------------------------
    class Subdivision(models.TextChoices):
        # --- BLOQUE COMUNICATIVO: ARCH_LANG (SUB-LIN-INSTR) ---
        SD_READ  = 'SD_READ',  _('Comprensión Lectora (Reading — CLM-UGR)')
        SD_LIST  = 'SD_LIST',  _('Comprensión Auditiva (Listening — CLM-UGR)')
        SD_WRIT  = 'SD_WRIT',  _('Expresión e Interacción Escritas (Writing — CLM-UGR)')
        SD_SPEAK = 'SD_SPEAK', _('Expresión e Interacción Orales (Speaking — CLM-UGR)')

        # --- BLOQUE LENGUAS MINOR (SUB-LIN-MINOR) ---
        SD_PHON_GRAPH    = 'SD_PHON_GRAPH',    _('Grafía y Fonética (Minor/Lenguas No Latinas)')
        SD_MORPH_BASE    = 'SD_MORPH_BASE',    _('Morfosintaxis y Estructura Elemental (Minor)')
        SD_LEX_COMM      = 'SD_LEX_COMM',      _('Léxico y Función Comunicativa (Minor)')
        SD_READ_ADAP     = 'SD_READ_ADAP',     _('Comprensión Lectora Adaptada (Minor)')
        SD_CULT_INTEGRITY = 'SD_CULT_INTEGRITY', _('Competencia Intercultural y Contexto (Minor)')

        # --- BLOQUE FILOLÓGICO (SUB-LIN-PHILO) ---
        SD_PHONO      = 'SD_PHONO',      _('Fonética y Fonología Histórica (Philo UGR)')
        SD_MORPH_DIAC = 'SD_MORPH_DIAC', _('Morfología Diacrónica (Philo UGR)')
        SD_LEX_SEM    = 'SD_LEX_SEM',    _('Lexicología y Semántica Histórica (Philo UGR)')

        # --- BLOQUE ECDÓTICO (SUB-LIN-ECDO) ---
        SD_ORTOTYPO = 'SD_ORTOTYPO', _('Corrección Ortotipográfica (Ecdo UGR)')
        SD_STYLE    = 'SD_STYLE',    _('Corrección de Estilo Editorial (Ecdo UGR)')
        SD_ANNOT    = 'SD_ANNOT',    _('Anotación Crítica y Edición Científica (Ecdo UGR)')
        SD_EVAL     = 'SD_EVAL',     _('Evaluación Editorial e Informe de Lector (Ecdo UGR)')

        # --- BLOQUE NORMATIVO (SUB-LIN-NORM) ---
        SD_CORPUS_ANALYSIS  = 'SD_CORPUS_ANALYSIS',  _('Investigación y Validación Empírica (Norm UGR)')
        SD_MORPH_ANTINORM   = 'SD_MORPH_ANTINORM',   _('Diagnóstico de Desviaciones Morfosintácticas')
        SD_ORTHO_PRESCRIPTIVE = 'SD_ORTHO_PRESCRIPTIVE', _('Ortografía y Ortotipografía Académica')
        SD_CRITICAL_NORM    = 'SD_CRITICAL_NORM',    _('Comentario Crítico y Justificación Bibliográfica')

        # --- BLOQUE TRADUCCIÓN TÉCNICA (SUB-LIN-TRA-TECH) ---
        SD_TRA_ANALYSIS  = 'SD_TRA_ANALYSIS',  _('Análisis del Encargo Traductológico')
        SD_TERM_RESEARCH = 'SD_TERM_RESEARCH', _('Documentación Terminológica y Glosario')
        SD_TRA_DRAFT     = 'SD_TRA_DRAFT',     _('Traducción Directa Cronometrada')

        # --- BLOQUE TRADUCCIÓN LITERARIA (SUB-LIN-TRA-LIT) ---
        SD_TRA_STYLE    = 'SD_TRA_STYLE',    _('Análisis Estilístico Comparado (TRA-LIT)')
        SD_TRA_CREATIVE = 'SD_TRA_CREATIVE', _('Transferencia Estética (TRA-LIT)')
        SD_TRA_CRIT     = 'SD_TRA_CRIT',     _('Comentario Exegético y Justificación Traductológica')

        # --- BLOQUE HUMANIDADES HISTORIA (SUB-HUM-HIST) ---
        SD_HIST_DEV  = 'SD_HIST_DEV',  _('Desarrollo Historiográfico — Prueba Escrita')
        SD_HIST_PRAC = 'SD_HIST_PRAC', _('Análisis de Fuentes y Comentario Documental')

        # --- BLOQUE HUMANIDADES FILOSOFÍA (SUB-HUM-PHIL) ---
        SD_PHIL_TEST  = 'SD_PHIL_TEST',  _('Test de Precisión Conceptual (Filosofía UGR)')
        SD_PHIL_DEV   = 'SD_PHIL_DEV',   _('Preguntas de Desarrollo (Filosofía UGR)')
        SD_PHIL_TEXT  = 'SD_PHIL_TEXT',  _('Comentario de Texto Filosófico (UGR)')
        SD_PHIL_ESSAY = 'SD_PHIL_ESSAY', _('Ensayo Filosófico Argumentado (UGR)')

        # --- BLOQUE HUMANIDADES ARTE (SUB-HUM-ART-HIST / ART-CREA) ---
        SD_ART_IDENT = 'SD_ART_IDENT', _('Reconocimiento Iconográfico de Imágenes')
        SD_ART_ANAL  = 'SD_ART_ANAL',  _('Análisis Formal e Iconológico — Panofsky')
        SD_CREA_PORT = 'SD_CREA_PORT', _('Portafolio Digital de Proceso Creativo')
        SD_CREA_MEM  = 'SD_CREA_MEM',  _('Memoria de Proceso y Análisis Crítico')

        # --- BLOQUE HUMANIDADES MÚSICA (SUB-HUM-MUS) ---
        SD_MUS_LIST  = 'SD_MUS_LIST',  _('Identificación Auditiva Musical')
        SD_MUS_SCORE = 'SD_MUS_SCORE', _('Análisis en Partitura (Armónico y Formal)')

        # --- BLOQUE HUMANIDADES ANTROPOLOGÍA (SUB-HUM-ANTH) ---
        SD_ANTH_TEXT  = 'SD_ANTH_TEXT',  _('Comentario de Fuente Etnográfica o Texto Antr.')
        SD_ANTH_ESSAY = 'SD_ANTH_ESSAY', _('Disertación Comparativa Intercultural')

        # --- BLOQUE SALUD MEDICINA (SUB-SAN-MED-*) ---
        SD_ANAMNESIS       = 'SD_ANAMNESIS',       _('Anamnesis y Entrevista Clínica')
        SD_SYNDROME_BUILD  = 'SD_SYNDROME_BUILD',  _('Identificación Sindrómica')
        SD_DIFF_DIAGNOSIS  = 'SD_DIFF_DIAGNOSIS',  _('Diagnóstico Diferencial')
        SD_CLINICAL_PRIORITY = 'SD_CLINICAL_PRIORITY', _('Priorización Clínica y Actuación')
        SD_ECOE_STATION    = 'SD_ECOE_STATION',    _('Estación ECOE Cronometrada')
        SD_ANAT_MACRO      = 'SD_ANAT_MACRO',      _('Anatomía Macroscópica — Nomenclatura TAI')
        SD_ANAT_RADIO      = 'SD_ANAT_RADIO',      _('Anatomía Radiológica — Semiología RX/RM/TC')
        SD_HISTO_MICRO     = 'SD_HISTO_MICRO',     _('Histología Microscópica — Identificación Tisular')
        SD_HISTO_FORMULA   = 'SD_HISTO_FORMULA',   _('Fórmula Leucocitaria — Identificación Morfológica')
        SD_FISIO_HOMEO     = 'SD_FISIO_HOMEO',     _('Homeostasis y SNA — Fisiología General')
        SD_FISIO_CARDIO    = 'SD_FISIO_CARDIO',    _('Fisiología Cardiovascular (UGR)')
        SD_FISIO_ECG       = 'SD_FISIO_ECG',       _('Electrocardiografía — Trazado Normal')
        SD_FISIO_RESP      = 'SD_FISIO_RESP',      _('Fisiología Respiratoria y Espirometría')
        SD_FISIO_RENAL     = 'SD_FISIO_RENAL',     _('Fisiología Renal y Equilibrio Ácido-Base')

        # --- BLOQUE SALUD ESPECIALIDADES (Enfermería, Odonto, Fisio, Bioquim, Farm, Psy, Vet, Nut) ---
        SD_CUID_NANDA        = 'SD_CUID_NANDA',        _('Diagnóstico NANDA/NIC/NOC y Plan de Cuidados')
        SD_CUID_SAFETY       = 'SD_CUID_SAFETY',       _('Protocolo de Seguridad en Técnicas Enfermeras')
        SD_ODON_RADIO        = 'SD_ODON_RADIO',        _('Radiología Dental — Ortopantomografía')
        SD_ODON_PROC         = 'SD_ODON_PROC',         _('Procedimiento Técnico Odontológico')
        SD_FISIO_VAL         = 'SD_FISIO_VAL',         _('Valoración Funcional — Fisioterapia')
        SD_FISIO_PALP        = 'SD_FISIO_PALP',        _('Anatomía Palpatoria — Puntos Gatillo')
        SD_BIOQUIM_METAB     = 'SD_BIOQUIM_METAB',     _('Bioquímica Metabólica — Rutas Metabólicas')
        SD_BIOQUIM_LAB       = 'SD_BIOQUIM_LAB',       _('Prácticas de Laboratorio Bromatológico (EP)')
        SD_FARM_FUNDA        = 'SD_FARM_FUNDA',        _('Fundamentos de Farmacología — Mecanismo de Acción')
        SD_FARM_CLINICA      = 'SD_FARM_CLINICA',      _('Farmacología Clínica — Selección y Dosificación')
        SD_PSY_DIAG          = 'SD_PSY_DIAG',          _('Diagnóstico DSM-5/CIE-11 — Psicopatología del Adulto')
        SD_PSY_EVAL_TECH     = 'SD_PSY_EVAL_TECH',     _('Evaluación Psicológica: Técnicas y Aplicaciones')
        SD_PSY_MET_DESIGN    = 'SD_PSY_MET_DESIGN',    _('Métodos y Diseños de Investigación (Psicología)')
        SD_PSY_STAT_DATA     = 'SD_PSY_STAT_DATA',     _('Descripción y Exploración de Datos Psicológicos')
        SD_VET_CLIN          = 'SD_VET_CLIN',          _('Clínica Animal — Diagnóstico Veterinario (UCO)')
        SD_VET_CIR           = 'SD_VET_CIR',           _('Cirugía Veterinaria — Procedimientos (UCO)')
        SD_NUT_DISENO        = 'SD_NUT_DISENO',        _('Diseño y Evaluación de Dietas — Dietética UGR')
        SD_NUT_VALORACION    = 'SD_NUT_VALORACION',    _('Valoración del Estado Nutricional (UGR)')
        SD_BROM_COMPOSICION  = 'SD_BROM_COMPOSICION',  _('Composición y Valor Nutricional de Alimentos')
        SD_BROM_ALTERACIONES = 'SD_BROM_ALTERACIONES', _('Alteraciones, Adulteraciones y Calidad Alimentaria')
        SD_SPUB_EPIDEMIOLOGIA = 'SD_SPUB_EPIDEMIOLOGIA', _('Epidemiología Nutricional y Vigilancia Alimentaria')
        SD_SPUB_EDUCACION    = 'SD_SPUB_EDUCACION',    _('Programas de Educación Nutricional y Comedores')
        SD_SPUB_COLECTIVIDADES = 'SD_SPUB_COLECTIVIDADES', _('Gestión Alimentación en Colectividades')

        # --- BLOQUE CSJ DERECHO (SUB-SOC-LAW-*) ---
        SD_PROC_CIV_PRINCIPIOS = 'SD_PROC_CIV_PRINCIPIOS', _('Principios y Presupuestos Procesales Civiles')
        SD_PROC_CIV_DEMANDA    = 'SD_PROC_CIV_DEMANDA',    _('Demanda, Contestación y Proceso Declarativo')
        SD_PROC_CIV_EXEC       = 'SD_PROC_CIV_EXEC',       _('Ejecución Forzosa Civil')
        SD_PROC_CIV_CAUTELAR   = 'SD_PROC_CIV_CAUTELAR',   _('Medidas Cautelares Civiles')
        SD_PROC_PEN_INVEST     = 'SD_PROC_PEN_INVEST',     _('Instrucción e Investigación Penal')
        SD_PROC_PEN_CAU        = 'SD_PROC_PEN_CAU',        _('Medidas Cautelares Penales')
        SD_PROC_PEN_INTER      = 'SD_PROC_PEN_INTER',      _('Fase Intermedia y Sobreseimiento Penal')
        SD_PROC_PEN_JUICIO     = 'SD_PROC_PEN_JUICIO',     _('Juicio Oral Penal — Principios y Prueba')
        SD_PROC_PEN_SENT       = 'SD_PROC_PEN_SENT',       _('Sentencia Penal y Cosa Juzgada')
        SD_PROC_PEN_TIPOS      = 'SD_PROC_PEN_TIPOS',      _('Tipología de Procesos Penales')
        SD_PROC_PEN_REC        = 'SD_PROC_PEN_REC',        _('Recursos Penales y Ejecución de Sentencia')
        SD_DICT_CIV_PERSONA    = 'SD_DICT_CIV_PERSONA',    _('Persona, Familia y Derecho Civil General')
        SD_DICT_CIV_OBLIG      = 'SD_DICT_CIV_OBLIG',      _('Obligaciones y Contratos Civiles')
        SD_DICT_CIV_REAL       = 'SD_DICT_CIV_REAL',       _('Derechos Reales y Propiedad')
        SD_DICT_PEN_TIPOS      = 'SD_DICT_PEN_TIPOS',      _('Tipos Penales y Bien Jurídico Protegido')
        SD_DICT_PEN_CIRC       = 'SD_DICT_PEN_CIRC',       _('Circunstancias Modificativas de la Responsabilidad')
        SD_DICT_PEN_CONCURSO   = 'SD_DICT_PEN_CONCURSO',   _('Concurso de Delitos y Penas')

        # --- BLOQUE CSJ ECONOMÍA/ADE (SUB-SOC-ECON-*) ---
        SD_STAT_FUND      = 'SD_STAT_FUND',      _('Estadística y Técnicas Cuantitativas — Fundamentos')
        SD_ECON_REGRESION = 'SD_ECON_REGRESION', _('Econometría: Regresión y MCO')
        SD_ECON_SERIES    = 'SD_ECON_SERIES',    _('Econometría: Series Temporales y Predicción')
        SD_ACC_FUND       = 'SD_ACC_FUND',       _('Contabilidad Financiera — Fundamentos')
        SD_ACC_ANALISIS   = 'SD_ACC_ANALISIS',   _('Análisis de Estados Financieros')
        SD_STR_ANALISIS   = 'SD_STR_ANALISIS',   _('Análisis Estratégico del Entorno')
        SD_STR_FORMULA    = 'SD_STR_FORMULA',    _('Formulación e Implantación Estratégica')
        SD_MICRO_FUND     = 'SD_MICRO_FUND',     _('Microeconomía — Teoría del Consumidor y Empresa')
        SD_MACRO_FUND     = 'SD_MACRO_FUND',     _('Macroeconomía — Modelos de Equilibrio')

        # --- BLOQUE CSJ EDUCACIÓN (SUB-SOC-EDU-*) ---
        SD_EDU_DUA       = 'SD_EDU_DUA',       _('Diseño Universal para el Aprendizaje (DUA/LOMLOE)')
        SD_EDU_SITUACION = 'SD_EDU_SITUACION', _('Situación de Aprendizaje y Programación Didáctica')
        SD_EDU_MAES_PROC = 'SD_EDU_MAES_PROC', _('Procesos y Contextos Educativos — MAES UGR')
        SD_EDU_MAES_DID  = 'SD_EDU_MAES_DID',  _('Didáctica Específica — MAES UGR')

        # --- BLOQUE CSJ COMUNICACIÓN (SUB-SOC-COMM-*) ---
        SD_JOUR_REDACCION = 'SD_JOUR_REDACCION', _('Redacción Periodística y Géneros Informativos')
        SD_JOUR_ETICA     = 'SD_JOUR_ETICA',     _('Ética, Deontología y Verificación (Periodismo)')
        SD_AV_GUION       = 'SD_AV_GUION',       _('Guion Audiovisual — Literario y Técnico')
        SD_AV_REALIZACION = 'SD_AV_REALIZACION', _('Técnica de Realización y Postproducción')

        # --- BLOQUE CSJ GEOGRAFÍA (SUB-SOC-GEOG-*) ---
        SD_GEOG_SIG_ANALISIS = 'SD_GEOG_SIG_ANALISIS', _('Análisis SIG y Cartografía Digital')
        SD_GEOG_TER_ANALISIS = 'SD_GEOG_TER_ANALISIS', _('Análisis Territorial y Demografía')
        SD_GEOG_FIS_CLIMA    = 'SD_GEOG_FIS_CLIMA',    _('Climatología y Geomorfología')

        # --- BLOQUE CSJ TRABAJO SOCIAL (SUB-SOC-WORK-*) ---
        SD_WORK_INT_PRAC = 'SD_WORK_INT_PRAC', _('Intervención Social — Práctica y Diagnóstico')
        SD_WORK_INT_THEO = 'SD_WORK_INT_THEO', _('Intervención Social — Teoría y Modelos')
        SD_WORK_POL_PRAC = 'SD_WORK_POL_PRAC', _('Política Social — Análisis Crítico Práctico')
        SD_WORK_POL_THEO = 'SD_WORK_POL_THEO', _('Política Social — Estado de Bienestar y Modelos')
        SD_WORK_MED_PRAC = 'SD_WORK_MED_PRAC', _('Mediación Social — Supuestos Prácticos')
        SD_WORK_MED_THEO = 'SD_WORK_MED_THEO', _('Mediación Social — Teoría y Modelos')

        # --- BLOQUE INGENIERÍA (SUB-TEC-*) ---
        SD_SOFT_ALG   = 'SD_SOFT_ALG',   _('Algoritmia y Complejidad Computacional')
        SD_SOFT_DEBUG = 'SD_SOFT_DEBUG', _('Depuración, Optimización y Patrones de Diseño')
        SD_SOFT_SE    = 'SD_SOFT_SE',    _('Ingeniería del Software — Requisitos y Arquitectura')
        SD_CIVIL_CALC = 'SD_CIVIL_CALC', _('Cálculo de Estructuras — Esfuerzos y Dimensionado')
        SD_CIVIL_NORM = 'SD_CIVIL_NORM', _('Cumplimiento Normativo Estructural (CTE/EHE)')
        SD_INDUS_TERM = 'SD_INDUS_TERM', _('Termodinámica y Ciclos de Potencia')
        SD_INDUS_TMM  = 'SD_INDUS_TMM',  _('Teoría de Máquinas — Cinemática y Dinámica')
        SD_CHEM_BAL   = 'SD_CHEM_BAL',   _('Balances de Materia y Energía en Procesos Químicos')
        SD_CHEM_REACT = 'SD_CHEM_REACT', _('Diseño de Reactores y Cinética Química')
        SD_ARCH_PROJ  = 'SD_ARCH_PROJ',  _('Proyecto Arquitectónico — Composición y Programa')
        SD_URB_PLAN   = 'SD_URB_PLAN',   _('Planeamiento Urbanístico y Ordenación del Territorio')
        SD_CONS_TECH  = 'SD_CONS_TECH',  _('Sistemas Constructivos y Detalle Técnico')
        SD_CONS_MAN   = 'SD_CONS_MAN',   _('Gestión de Obra — Planificación y Seguridad')
        SD_MATH_PROOF = 'SD_MATH_PROOF', _('Demostración Matemática Formal — Análisis y Álgebra')
        SD_MATH_PROB  = 'SD_MATH_PROB',  _('Resolución de Problemas Matemáticos Estructurales')

        # --- BLOQUE CIENCIAS PURAS (SUB-SCI-*) ---
        SD_BIO_TEORÍA   = 'SD_BIO_TEORIA',  _('Fundamentos Biológicos — Teoría y Concepto')
        SD_BIO_GENETIC  = 'SD_BIO_GENETIC', _('Genética, Evolución y Ecología — Problemas')
        SD_CHEM_TEORIA  = 'SD_CHEM_TEORIA', _('Química Pura — Fundamentos Teóricos')
        SD_CHEM_SINTESIS = 'SD_CHEM_SINTESIS', _('Síntesis y Reactividad Química — Problemas')
        SD_PHYS_TEORIA  = 'SD_PHYS_TEORIA', _('Física — Principios y Leyes Fundamentales')
        SD_PHYS_CALC    = 'SD_PHYS_CALC',   _('Física — Resolución Analítica de Problemas')
        SD_GEOL_IDENT   = 'SD_GEOL_IDENT',  _('Identificación Mineralógica y Petrológica')
        SD_GEOL_STRAT   = 'SD_GEOL_STRAT',  _('Estratigrafía y Lectura de Columnas')
        SD_GEOL_CARTOG  = 'SD_GEOL_CARTOG', _('Cartografía Geológica e Interpretación de Cortes')
        SD_ENV_GESTIÓN  = 'SD_ENV_GESTION', _('Gestión de Residuos y Evaluación de Impacto')
        SD_ENV_CONTAM   = 'SD_ENV_CONTAM',  _('Contaminación — Fuentes, Dispersión y Control')
        SD_DATA_PROB    = 'SD_DATA_PROB',   _('Probabilidad y Modelos Estadísticos (UCM GIDIA)')
        SD_DATA_INF     = 'SD_DATA_INF',    _('Inferencia Estadística y Contrastes de Hipótesis')
        SD_DATA_REG     = 'SD_DATA_REG',    _('Regresión y Análisis Multivariante')
        SD_ML_SUPER     = 'SD_ML_SUPER',    _('Aprendizaje Supervisado — Clasificación y Regresión')
        SD_ML_UNSUPER   = 'SD_ML_UNSUPER',  _('Aprendizaje No Supervisado y Evaluación de Modelos')
        SD_ML_DEEP      = 'SD_ML_DEEP',     _('Aprendizaje Profundo y Fundamentos de IA')
        SD_BIG_ADQUI    = 'SD_BIG_ADQUI',   _('Adquisición, Limpieza y Almacenamiento de Datos')
        SD_BIG_PROC     = 'SD_BIG_PROC',    _('Procesamiento Distribuido — Hadoop/Spark/Streaming')
        SD_BIG_ARCH     = 'SD_BIG_ARCH',    _('Arquitectura de Sistemas de Datos — Lambda/Kappa')

        # --- BLOQUE RESOLUTIVO GENÉRICO (Ingeniería/Ciencias — fallback) ---
        SD_THEO  = 'SD_THEO',  _('Validación Teórica — Axiomas y Principios')
        SD_MODEL = 'SD_MODEL', _('Modelado Formal — Abstracción Matemática/Lógica')
        SD_CALC  = 'SD_CALC',  _('Precisión Algorítmica — Cálculo Procedimental')
        SD_VERIF = 'SD_VERIF', _('Verificación Normativa — Coherencia y Cumplimiento')

        # --- BLOQUE ASISTENCIAL/JURÍDICO GENÉRICO (Salud/Derecho — fallback) ---
        SD_FACT = 'SD_FACT', _('Extracción y Jerarquización de Hechos Relevantes')
        SD_NORM = 'SD_NORM', _('Encuadre en Ordenamiento Legal o Protocolo Clínico')
        SD_PROC = 'SD_PROC', _('Ejecución Procedimental — Tramitación o Maniobra Clínica')
        SD_ETHI = 'SD_ETHI', _('Evaluación Deontológica — Bioética o Seguridad Jurídica')

        # --- BLOQUE CRÍTICO/ARTÍSTICO GENÉRICO (Humanidades — fallback) ---
        SD_SOURCE = 'SD_SOURCE', _('Crítica de Fuentes Primarias — Análisis Documental')
        SD_DISC   = 'SD_DISC',   _('Construcción Discursiva — Ensayo Crítico Argumentado')
        SD_ARTE   = 'SD_ARTE',   _('Validación Artística — Técnica Matérica y Composición')

    # -------------------------------------------------------------------------
    # Fields / Campos
    # -------------------------------------------------------------------------
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name='sections',
        verbose_name=_('Examen')
    )
    subdivision_id = models.CharField(
        _('ID Subdivisión'), max_length=60, choices=Subdivision.choices,
        help_text=_('Identificador técnico de la subdivisión. Ref: V06DOC_SUBDIVISIONS.')
    )
    title        = models.CharField(_('Título de la Sección'), max_length=255)
    instructions = models.TextField(_('Instrucciones para el Alumno'))
    order        = models.PositiveSmallIntegerField(_('Orden'), default=0)
    time_limit   = models.PositiveIntegerField(
        _('Límite de Tiempo (s)'), default=0,
        help_text=_('Segundos. 0 = sin límite. Non-Backtracking activo si > 0.')
    )

    # Stimulus and layout / Estímulo y distribución visual
    # Ref: V06DOC_TEMPLATES Sección 2 (section_stimulus, layout_mode)
    section_stimulus = models.TextField(
        _('Estímulo de Sección'), blank=True, null=True,
        help_text=_(
            'Texto, HTML o URL de imagen que sirve de contexto compartido para toda la sección. '
            'Se renderiza en el Panel Lateral Persistente (SPLIT_TEXT/SPLIT_VISUAL). '
            'Ejemplos: texto de lectura (Reading), caso clínico, fuente histórica, partitura URL.'
        )
    )
    layout_mode = models.CharField(
        _('Modo de Layout'), max_length=20,
        choices=LayoutMode.choices, default=LayoutMode.STANDARD,
        help_text=_(
            'STANDARD: ancho completo. '
            'SPLIT_TEXT: panel lateral de texto (Reading/Caso). '
            'SPLIT_VISUAL: panel lateral visual (Imagen/Arte/Partitura).'
        )
    )

    class Meta:
        ordering    = ['order']
        verbose_name = _('Sección de Examen')
        verbose_name_plural = _('Secciones de Examen')

    def __str__(self):
        return f"[{self.subdivision_id}] {self.title} (Examen: {str(self.exam.uuid)[:8]})"


class ExamItem(models.Model):
    """
    Atomic evaluation block. The minimum indivisible unit of assessment.
    Each item binds a Widget (UI component), a BlockType (evaluation motor),
    and the JSON contracts for content generation and grading.
    Ref: V06DOC_BLOCKS, V06DOC_WIDGETS, V06DOC_TEMPLATES, V06DOC_METADATA.
    ---
    Bloque de evaluación atómico. La unidad mínima indivisible de evaluación.
    Cada ítem vincula un Widget (componente UI), un BlockType (motor de evaluación),
    y los contratos JSON para generación de contenido y calificación.
    Ref: V06DOC_BLOCKS, V06DOC_WIDGETS, V06DOC_TEMPLATES, V06DOC_METADATA.
    """

    # -------------------------------------------------------------------------
    # Widget taxonomy — All widgets from V06DOC_WIDGETS (v5.9)
    # Taxonomía de widgets — Todos los widgets de V06DOC_WIDGETS (v5.9)
    # -------------------------------------------------------------------------
    class Widget(models.TextChoices):
        # Technical widgets (V06DOC_WIDGETS Sec 1)
        W_TECH_CALC   = 'W-TECH-CALC',   _('Consola de Cálculo Procedimental (Ingeniería/Ciencias)')
        W_CLIN_SCAN   = 'W-CLIN-SCAN',   _('Visor de Evidencia Diagnóstica — Zoom HD + Marcadores')
        W_OBJ_STRIKE  = 'W-OBJ-STRIKE',  _('Selector de Respuesta con Riesgo (PRM-STRIKE/RBT)')
        W_CASE_ECOE   = 'W-CASE-ECOE',   _('Estación Clínica ECOE Simulada — Secuencial Non-Backtracking')

        # Discursive & action widgets (V06DOC_WIDGETS Sec 2)
        W_HUM_TEXT    = 'W-HUM-TEXT',    _('Editor de Exégesis Crítica — Pantalla Dividida + Citas')
        W_PROC_ACTION = 'W-PROC-ACTION', _('Panel de Acción Crítica — Checklist de Seguridad')
        W_COMM_DIALOG = 'W-COMM-DIALOG', _('Chat Interactivo con UniversIA — Mediación Dialéctica')
        W_LAW_NAV     = 'W-LAW-NAV',     _('Navegador de Marco Normativo y Repositorios de Autoridad')
        W_PORTFOLIO   = 'W-PORTFOLIO',   _('Portafolio Digital de Proceso Creativo (Bellas Artes)')

        # Linguistic & structural widgets (V06DOC_WIDGETS Sec 3)
        W_TXT_CLOZE   = 'W-TXT-CLOZE',  _('Integrador de Huecos en Texto — Open/Multi-Choice Cloze')
        W_MIX_MATCH   = 'W-MIX-MATCH',  _('Matriz de Vinculación — Drag & Drop Emparejamiento')

        # Audio widget (V06DOC_WIDGETS Sec 6 — Instrumental/Musical)
        W_AUDIO_INSTR = 'W-AUDIO-INSTR', _('Reproductor de Audio — Contador de Reproducciones Hermético')

        # Specialized language widgets (V06DOC_WIDGETS Sec 5/7)
        W_PHILO_IPA       = 'W-PHILO-IPA',       _('Pad de Transcripción Fonética y Diacrónica (Philo UGR)')
        W_PHILO_ECDO      = 'W-PHILO-ECDO',      _('Editor de Crítica Textual y Colación (Ecdótica UGR)')
        W_PHILO_OCR_PALE  = 'W-PHILO-OCR-PALE',  _('Visor Paleográfico HD con Capa de Transcripción')
        W_CALLI_PAD       = 'W-CALLI-PAD',       _('Pad Caligráfico — Lenguas No Latinas (Ductus/OCR)')
        W_DOC_RESOURCES   = 'W-DOC-RESOURCES',   _('Panel de Recursos Documentales UGR (TRA-TECH)')

        # Multimedia & analysis widgets (V06DOC_WIDGETS Sec 8)
        W_MUS_SCORE   = 'W-MUS-SCORE',   _('Visor de Partitura + Análisis Armónico Anotable (HUM-MUS)')
        W_ART_IDENT   = 'W-ART-IDENT',   _('Visor Iconográfico HD — Identificación + Comentario Panofsky')

        # Layout helpers (V06DOC_WIDGETS — auxiliares)
        W_MEDI_LAYOUT   = 'W-MEDI-LAYOUT',   _('Interfaz Doble Panel para Transferencia (TRA-TECH/LIT)')
        W_OCR_PRO       = 'W-OCR-PRO',       _('Módulo de Auditoría de Producción Manuscrita (OCR)')
        W_INSTR_SELECTOR = 'W-INSTR-SELECTOR', _('Selector Multimodal CertAcles (Teclado/Trazos/OCR)')

    # -------------------------------------------------------------------------
    # Block type taxonomy — All motors from V06DOC_BLOCKS (v5.9)
    # Taxonomía de tipos de bloque — Todos los motores de V06DOC_BLOCKS (v5.9)
    # -------------------------------------------------------------------------
    class BlockType(models.TextChoices):
        # Objective & technical motors (V06DOC_BLOCKS Sec 1)
        PRM_STRIKE  = 'PRM-STRIKE',  _('Respuesta Múltiple con Penalización — Fórmula UGR [A-E/(N-1)]')
        RBT_CANON   = 'RBT-CANON',   _('Respuesta Breve de Precisión Terminológica — Sin Paráfrasis')
        RBT_SHORT_LANG = 'RBT-SHORT-LANG', _('Respuesta Breve Lingüística ≤4 palabras (CertAcles/CLM-UGR)')
        RPP_TRAZA   = 'RPP-TRAZA',   _('Resolución Procedimental con Arrastre de Error — Multietapa')

        # Security & critical analysis motors (V06DOC_BLOCKS Sec 2)
        CDS_KILL    = 'CDS-KILL',    _('Checklist Dicotómico de Seguridad Crítica — KILL_SWITCH')
        DRA_HOLO    = 'DRA-HOLO',    _('Rúbrica Analítica Holística — 4 Ejes UGR/CertAcles')
        DRA_HOLO_LIT = 'DRA-HOLO-LIT', _('Rúbrica Holística Literaria — 4 Ejes TRA-LIT FTI-UGR')
        BMT_SHIFT   = 'BMT-SHIFT',   _('Mediación y Transferencia de Registro — Fidelidad + Adecuación')
        ILC_CONTEXT = 'ILC-CONTEXT', _('Interpretación de Contexto y Datos Brutos (IA-Evaluado)')
        EV_PALE     = 'EV-PALE',     _('Transcripción y Exégesis de Fuentes Primarias (Paleografía)')

        # Specialized evaluation motors (V06DOC_BLOCKS Sec 4/6)
        EV_DIAC_VAL      = 'EV-DIAC-VAL',      _('Motor Diacrónico — Evolución Fonética (Philo UGR)')
        EV_NORM_ANALYSIS = 'EV-NORM-ANALYSIS',  _('Motor Panhispánico — Desviaciones Norma (Norm UGR)')
        EV_TRA_PRECISION = 'EV-TRA-PRECISION',  _('Motor Precisión Terminológica Traductológica')
        EV_TRA_PRECISION_TECH = 'EV-TRA-PRECISION-TECH', _('Motor Precisión FTI-UGR — Jerarquía Errores A/B/C')
        EV_ICON_ART      = 'EV-ICON-ART',      _('Motor Iconológico — Identificación + Panofsky (ART-HIST)')
        EV_MUS_ANAL      = 'EV-MUS-ANAL',      _('Motor de Análisis Musical Armónico-Formal (HUM-MUS)')

        # Linguistic & structural motors (V06DOC_BLOCKS Sec 3)
        CLO_OPEN    = 'CLO-OPEN',    _('Open Cloze / Rellenado Abierto — Validación Léxico-Morfológica')
        CLO_MULTI   = 'CLO-MULTI',   _('Multiple Choice Cloze / Rellenado Selectivo — Distractores')
        MAT_LINK    = 'MAT-LINK',    _('Matching / Emparejamiento — Drag & Drop Vinculación')
        DIA_INTERACT = 'DIA-INTERACT', _('Interacción Dialéctica Asistida por UniversIA — Oral/Chat')

    # -------------------------------------------------------------------------
    # Level requisite taxonomy / Taxonomía de requisito de nivel
    # Ref: V06DOC_METADATA Sec 3
    # -------------------------------------------------------------------------
    class LevelRequisite(models.TextChoices):
        MANDATORY = 'MANDATORY', _('Obligatorio — Todos los niveles')
        OPTIONAL  = 'OPTIONAL',  _('Opcional — Enriquecimiento no evaluable')
        ADVANCED  = 'ADVANCED',  _('Avanzado — Solo LVL_C o ITIN_MAI/INV')

    # -------------------------------------------------------------------------
    # Fail logic taxonomy / Taxonomía de lógica de fallo
    # Ref: V06DOC_METADATA Sec 3
    # -------------------------------------------------------------------------
    class FailLogic(models.TextChoices):
        PENALTY      = 'PENALTY',      _('Penalización Estándar — Descuento Proporcional')
        FATAL        = 'FATAL',        _('Error Fatal — Nota 0 en la Sección/Destreza Completa')
        PARTIAL      = 'PARTIAL',      _('Crédito Parcial — Penalización Proporcional al Error')
        PARTIAL_RETRY = 'PARTIAL_RETRY', _('Reintento Parcial — Solo Destreza Suspensa (CertAcles)')

    # -------------------------------------------------------------------------
    # Feedback taxonomy / Taxonomía de feedback
    # Ref: V06DOC_METADATA Sec 4
    # -------------------------------------------------------------------------
    class FeedbackTaxonomy(models.TextChoices):
        FB_CONCEPT    = 'FB_CONCEPT',    _('Error Conceptual — Falta de Base Teórica')
        FB_FORMAL     = 'FB_FORMAL',     _('Error Formal de Registro, Sintaxis u Ortotipografía')
        FB_PROCEDURAL = 'FB_PROCEDURAL', _('Error Procedimental — Método o Secuencia Lógica')
        FB_SAFETY     = 'FB_SAFETY',     _('Violación de Protocolos Críticos de Seguridad')

    # -------------------------------------------------------------------------
    # Competency domain taxonomy / Taxonomía de dominio de competencia
    # Ref: V06DOC_METADATA Sec 1
    # -------------------------------------------------------------------------
    class CompetencyDomain(models.TextChoices):
        COMP_GEN  = 'COMP_GEN',  _('Competencias Genéricas — Síntesis, Expresión, Organización')
        COMP_TRA  = 'COMP_TRA',  _('Competencias Transversales — Pensamiento Crítico, TIC, Ética')
        COMP_ESP  = 'COMP_ESP',  _('Competencias Específicas — Conocimiento Técnico Nuclear')
        COMP_PROF = 'COMP_PROF', _('Competencias Profesionales — Resolución de Problemas Reales')

    # -------------------------------------------------------------------------
    # Cognitive taxonomy (Bloom) / Taxonomía cognitiva (Bloom)
    # Ref: V06DOC_METADATA Sec 2
    # -------------------------------------------------------------------------
    class CognitiveTaxonomy(models.TextChoices):
        COG_REM  = 'COG_REM',  _('Recordar — Identificación de Conceptos y Datos')
        COG_UND  = 'COG_UND',  _('Comprender — Explicación e Interpretación')
        COG_APP  = 'COG_APP',  _('Aplicar — Uso de Información en Casos Prácticos')
        COG_ANA  = 'COG_ANA',  _('Analizar — Relación Lógica entre Componentes')
        COG_EVAL = 'COG_EVAL', _('Evaluar — Justificación de Posturas y Crítica')
        COG_CREA = 'COG_CREA', _('Crear — Generación de Propuestas Originales')

    # -------------------------------------------------------------------------
    # Fields / Campos
    # -------------------------------------------------------------------------
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    section = models.ForeignKey(
        ExamSection, on_delete=models.CASCADE, related_name='items',
        verbose_name=_('Sección')
    )

    # Widget and motor binding / Vinculación widget-motor
    # Ref: V06DOC_STRUCTURE (SCHEMA-PROMPT BINDING)
    block_type = models.CharField(
        _('Tipo de Bloque / Motor'), max_length=30, choices=BlockType.choices,
        help_text=_('Motor de evaluación. Ref: V06DOC_BLOCKS.')
    )
    widget_id = models.CharField(
        _('Widget de Interfaz'), max_length=30, choices=Widget.choices,
        help_text=_('Componente UI. Ref: V06DOC_WIDGETS.')
    )

    # Item technical attributes / Atributos técnicos del ítem
    # Ref: V06DOC_METADATA Sec 3
    level_requisite = models.CharField(
        _('Requisito de Nivel'), max_length=20,
        choices=LevelRequisite.choices, default=LevelRequisite.MANDATORY
    )
    weight = models.DecimalField(
        _('Peso Relativo'), max_digits=3, decimal_places=2, default=1.00,
        validators=[MinValueValidator(0.1), MaxValueValidator(1.0)],
        help_text=_('Peso del ítem en la calificación de la sección (0.1 – 1.0).')
    )
    estimated_time = models.PositiveIntegerField(
        _('Tiempo Estimado (s)'), default=0,
        help_text=_('Segundos de resolución esperada. Informativo para la UI.')
    )
    fail_logic = models.CharField(
        _('Lógica de Fallo'), max_length=20,
        choices=FailLogic.choices, default=FailLogic.PENALTY,
        help_text=_('Determina cómo se gestiona el error en este ítem. Ref: V06DOC_METADATA.')
    )

    # Segregated JSON contract / Contrato JSON segregado
    # Ref: V06DOC_TEMPLATES Sección 3 (ITEM_PAYLOAD)
    content = models.JSONField(
        _('Contenido del Ítem'), default=dict, blank=True,
        help_text=_(
            'Generado por la IA: stem, options, text_with_gaps, source_text, '
            'targets, media_assets, initial_scenario, cloze_options, etc.'
        )
    )
    grading_logic = models.JSONField(
        _('Lógica de Calificación'), default=dict, blank=True,
        help_text=_(
            'Generado por la IA: correct_answer, gap_solutions (dict {gap_id: answer}), '
            'pairs, step_matrix, keywords, feedback_justification.'
        )
    )
    metadata = models.JSONField(
        _('Metadatos Pedagógicos'), default=dict, blank=True,
        help_text=_(
            'competency_tag (COMP_*), cognitive_level (COG_*), task_instruction '
            '(instrucción de llenado para la IA — preservada tras la generación).'
        )
    )

    order = models.PositiveSmallIntegerField(_('Orden'), default=0)

    class Meta:
        ordering    = ['order']
        verbose_name = _('Ítem de Examen')
        verbose_name_plural = _('Ítems de Examen')

    def __str__(self):
        return f"[{self.block_type}] {self.widget_id} — Sección: {self.section.subdivision_id} ({str(self.uuid)[:8]})"


class Submission(models.Model):
    """
    Exam delivery and grading report. One-to-one with Exam.
    Stores the student's raw responses and the generated grading report.
    Ref: V06DOC_TEMPLATES (STUDENT_SUBMISSION + GRADING_REPORT).
    ---
    Entrega del examen e informe de calificación. Relación uno-a-uno con Exam.
    Almacena las respuestas brutas del alumno y el informe de calificación generado.
    Ref: V06DOC_TEMPLATES (STUDENT_SUBMISSION + GRADING_REPORT).
    """
    exam = models.OneToOneField(
        Exam, on_delete=models.CASCADE, related_name='submission',
        verbose_name=_('Examen')
    )

    # Student responses / Respuestas del alumno
    # Ref: V06DOC_TEMPLATES Sec 4 (STUDENT_SUBMISSION)
    # Structure: { "responses": { "<item_id>": <raw_input> } }
    student_responses = models.JSONField(
        _('Respuestas del Estudiante'), null=True,
        help_text=_('Contrato: {"responses": {"<item_id>": <raw_input>}}. raw_input varía por widget.')
    )

    # Grading report / Informe de calificación
    # Ref: V06DOC_TEMPLATES Sec 5 (GRADING_REPORT)
    # Structure: { "sections": [...], "global_flags": [...], "feedback_stats": {...}, "qualitative_summary": "..." }
    grading_report = models.JSONField(
        _('Informe de Calificación'), null=True,
        help_text=_(
            'Contrato: {"sections": [{"subdivision_id", "title", "items": [{"item_id", "item_score", '
            '"feedback_category", "justification", ...}], "section_score", "status"}], '
            '"global_flags": [...], "feedback_stats": {...}, "qualitative_summary": "..."}'
        )
    )

    # Per-section scores for gating logic / Notas por sección para lógica de gating
    # Ref: V06DOC_ARCHETYPES (Criterio de Éxito por Destreza — Non-Compensation Rule)
    section_scores = models.JSONField(
        _('Calificaciones por Sección'), null=True, blank=True,
        help_text=_('{ "<subdivision_id>": <score_0_to_1> }. Usado para gating no-compensación.')
    )

    final_score = models.DecimalField(
        _('Nota Final'), max_digits=5, decimal_places=4, null=True,
        help_text=_('Valor en rango 0.0000 – 1.0000. Multiplicar por 10 para escala UGR.')
    )
    passed = models.BooleanField(_('Superado'), default=False)

    submitted_at = models.DateTimeField(_('Entregado a las'), auto_now_add=True)
    graded_at    = models.DateTimeField(_('Calificado a las'), null=True, blank=True)

    class Meta:
        verbose_name        = _('Entrega de Examen')
        verbose_name_plural = _('Entregas de Exámenes')

    def __str__(self):
        return f"Entrega — Examen {str(self.exam.uuid)[:8]} — Nota: {self.final_score}"
