from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

class Assessment(models.Model):
    @property
    def is_minor_language(self):
        """Check if language is Minor via strategy. / Comprueba si es lengua Minor via estrategia."""
        if self.archetype == self.Archetype.LANGUAGES:
            # [HITO 6] UGR: Prioridad al itinerario explícito si existe
            if self.language_itinerary:
                return self.language_itinerary == "MINOR"
            try:
                from core.services.assessment_strategies.languages_strategy import is_minor_language
                return is_minor_language(self.content.title)
            except ImportError:
                return False
        return False


    class Archetype(models.TextChoices):
        LOGIC_TECH = "LOGIC_AND_TECH", "LOGIC & TECH (Ingeniería y Ciencias)"
        LANGUAGES = "CEFR_LANGUAGES", "CEFR LANGUAGES (Idiomas)"
        SOCIO_LEGAL = "SOCIO_LEGAL", "SOCIO LEGAL (Derecho y Sociales)"
        HEALTH = "HEALTH_SCIENCES", "HEALTH SCIENCES (Salud)"
        HUMANITIES = "HUMANITIES_ARTS", "HUMANITIES & ARTS (Arte y Letras)"

    class AssessmentStatus(models.TextChoices):
        PENDING = "PENDING", "Pendiente de Generación"
        PROCESSING = "PROCESSING", "Generando Cuestionario"
        COMPLETED = "COMPLETED", "Listo para Realizar"
        AWAITING_CORRECTION = "AWAITING_CORRECTION", "Pendiente de Corrección"
        CORRECTING = "CORRECTING", "Corrigiendo"
        RESULTS_AVAILABLE = "RESULTS_AVAILABLE", "Resultados Disponibles"
        EXPIRED_UNTAKEN = "EXPIRED_UNTAKEN", "Expirado (No Realizado)"
        CORRECTION_EXPIRED = "CORRECTION_EXPIRED", "Corrección Expirada"
        GENERATION_FAILED_RETRYABLE = "GENERATION_FAILED_RETRYABLE", "Fallo de Generación (Reintentable)"
        CORRECTION_FAILED_RETRYABLE = "CORRECTION_FAILED_RETRYABLE", "Fallo de Corrección (Reintentable)"
        GENERATION_FAILED_QUOTA = "GENERATION_FAILED_QUOTA", "Fallo de Generación (Cuota API)"
        GENERATION_FAILED_FATAL = "GENERATION_FAILED_FATAL", "Fallo Permanente de Generación"
        CORRECTION_FAILED_FATAL = "CORRECTION_FAILED_FATAL", "Fallo Permanente de Corrección"
        PAUSED = "PAUSED", "Pausada por el Administrador"
        CANCELLED = "CANCELLED", "Cancelada por Administrador"
        USER_CANCELLED = "USER_CANCELLED", "Cancelado por el Usuario"

    # [HITO 6] UGR: Itinerarios Lingüísticos
    ITINERARY_CHOICES = [
        ('MAIOR', 'Maior (Especialidad / C1)'),
        ('MINOR', 'Minor (Segunda Lengua / A1-B2)'),
    ]

    content_copy = models.ForeignKey("contents.ContentCopy", on_delete=models.CASCADE, related_name="assessments")
    content = models.ForeignKey("contents.ContentMaterial", on_delete=models.CASCADE, related_name="assessments", editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assessments")
    status = models.CharField(max_length=50, choices=AssessmentStatus.choices, default=AssessmentStatus.PENDING)
    archetype = models.CharField(max_length=20, choices=Archetype.choices, default=Archetype.HUMANITIES, db_index=True)
    
    # [HITO 6] Nuevo Campo para Itinerario
    language_itinerary = models.CharField(max_length=10, choices=ITINERARY_CHOICES, null=True, blank=True, verbose_name="Itinerario Lingüístico")
    
    prompt_data = models.JSONField(default=dict, blank=True)
    selection_range = models.JSONField(default=dict, blank=True, null=True)
    reading_stimulus = models.TextField(blank=True, null=True)
    listening_transcript = models.TextField(blank=True, null=True)
    generated_audio = models.FileField(upload_to='assessment/generated_audio/%Y/%m/', blank=True, null=True, help_text="Audio nativo generado por Gemini 2.5")
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    results_expiration_date = models.DateTimeField(null=True, blank=True)
    total_questions_expected = models.PositiveIntegerField(default=0)
    questions_processed = models.PositiveIntegerField(default=0)
    was_viewed = models.BooleanField(default=False)
    last_error = models.TextField(blank=True, null=True)
    event_log = models.JSONField(default=list, blank=True)
    rejected_archetypes = models.JSONField(default=list, blank=True, help_text="Lista de arquetipos rechazados explícitamente por el usuario")

    def add_log_event(self, message, level="INFO"):
        entry = {"timestamp": timezone.now().isoformat(), "level": level, "message": str(message)}
        if not isinstance(self.event_log, list): self.event_log = []
        self.event_log.insert(0, entry)
        self.event_log = self.event_log[:50]
        self.save(update_fields=["event_log"])

    def save(self, *args, **kwargs):
        if self.content_copy and not self.content_id:
            self.content = self.content_copy.original_content
        
        # Evitamos import circular dentro del método si es posible, o usamos string reference
        # Pero para obtener settings globales, lo hacemos aquí
        from .models import AssessmentSettings
        try:
            app_settings = AssessmentSettings.get_settings()
            expiration_secs = app_settings.assessment_expiration_seconds
            results_days = app_settings.results_expiration_days
        except:
            expiration_secs = 86400
            results_days = 7

        if self.status == self.AssessmentStatus.COMPLETED and not self.expiration_date:
            self.expiration_date = timezone.now() + timedelta(seconds=expiration_secs)
        elif self.status == self.AssessmentStatus.RESULTS_AVAILABLE and not self.results_expiration_date:
            self.results_expiration_date = timezone.now() + timedelta(days=results_days)
            
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "1. Listado de Evaluaciones"
        ordering = ["-created_at"]


class Question(models.Model):
    class SourceType(models.TextChoices):
        DIRECT = "SRC_DIR", "Directo (Sin estímulo)"
        TEXT = "SRC_TXT", "Texto / Reading"
        AUDIO = "SRC_AUD", "Audio MP3 / Listening"
        IMAGE = "SRC_IMG", "Imagen / Fotografía"
        HYBRID = "SRC_HYB", "Híbrido (Texto + Audio)"

    class InteractionType(models.TextChoices):
        SELECTION = "QT_SEL", "Selección Simple (Test)"
        MATCHING = "QT_MATCH", "Emparejamiento"
        CLOZE_OPTIONS = "QT_CLZ_OPT", "Cloze con Opciones"
        CLOZE_OPEN = "QT_CLZ_OPN", "Cloze Abierto"
        TRANSFORMATION = "QT_TRF", "Transformación (Re-writing)"
        PRODUCTION = "QT_PROD", "Producción Libre"
        ORDERING = "QT_ORDER", "Ordenación"

    class ResponseMode(models.TextChoices):
        RADIO = "REQ_RADIO", "Radio Buttons"
        DROPDOWN = "REQ_DROP", "Desplegables inline"
        INPUT = "REQ_INPUT", "Caja de texto inline"
        DUAL = "REQ_DUAL", "Escritura Dual (Texto + Archivo)"
        RECORDER = "REQ_REC", "Grabadora Multimedia"
        MATCHING = "REQ_MATCH", "Matriz de Emparejamiento"
        ORDERING = "REQ_ORDER", "Lista de Ordenación"

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="questions")
    section_label = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cabecera de Sección")
    
    # Ejes del Santo Grial
    source_type = models.CharField(max_length=50, choices=SourceType.choices, default=SourceType.DIRECT)
    interaction_type = models.CharField(max_length=50, choices=InteractionType.choices, default=InteractionType.PRODUCTION)
    response_mode = models.CharField(max_length=50, choices=ResponseMode.choices, default=ResponseMode.DUAL)
    
    question_text = models.TextField()
    model_answer = models.TextField()
    options = models.JSONField(default=list, blank=True, help_text="Opciones para Test o Cloze")
    
    @property
    def requires_audio(self):
        return self.source_type in [self.SourceType.AUDIO, self.SourceType.HYBRID]

    @property
    def requires_recording(self):
        return self.response_mode == self.ResponseMode.RECORDER

    @property
    def requires_upload(self):
        return self.response_mode == self.ResponseMode.DUAL

    @property
    def is_cloze(self):
        return self.interaction_type in [self.InteractionType.CLOZE_OPTIONS, self.InteractionType.CLOZE_OPEN]

    @property
    def display_text(self):
        # Limpieza de posibles tags de control antiguos
        return self.question_text.replace("[---RECORDING-REQUIRED---]", "").replace("[---AUDIO-REQUIRED---]", "").strip()

    class Meta:
        verbose_name = "Pregunta (Emulador UGR)"
        verbose_name_plural = "2. Banco de Preguntas"
        ordering = ["id"]


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="user_answers")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer_text = models.TextField()
    attachment = models.FileField(upload_to='assessment/attachments/%Y/%m/', blank=True, null=True)
    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    answered_at = models.DateTimeField(auto_now_add=True)
    correction_expiration_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        verbose_name = "Respuesta de Alumno"
        verbose_name_plural = "3. Respuestas Recibidas"

class AssessmentSettings(models.Model):
    is_running = models.BooleanField(default=False)
    daily_limit = models.PositiveIntegerField(default=1)
    weekly_limit = models.PositiveIntegerField(default=3)
    assessment_expiration_seconds = models.PositiveIntegerField(default=86400)
    results_expiration_days = models.PositiveIntegerField(default=7)
    last_run_timestamp = models.DateTimeField(null=True, blank=True)
    last_run_status = models.TextField(blank=True)
    event_log = models.JSONField(default=list, blank=True)
    
    def save(self, *args, **kwargs): 
        self.pk = 1
        super().save(*args, **kwargs)
        
    @classmethod
    def get_settings(cls): 
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
        
    class Meta:
        verbose_name = "Ajuste de Motor"
        verbose_name_plural = "0. Configuración del Motor"
