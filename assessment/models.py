from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

class Assessment(models.Model):
    class Archetype(models.TextChoices):
        SCIENCES = "SCIENCES", "Ciencias Exactas"
        LANGUAGES = "LANGUAGES", "Idiomas"
        HUMANITIES = "HUMANITIES", "Humanidades"

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

    content_copy = models.ForeignKey("contents.ContentCopy", on_delete=models.CASCADE, related_name="assessments")
    content = models.ForeignKey("contents.ContentMaterial", on_delete=models.CASCADE, related_name="assessments", editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assessments")
    status = models.CharField(max_length=50, choices=AssessmentStatus.choices, default=AssessmentStatus.PENDING)
    archetype = models.CharField(max_length=20, choices=Archetype.choices, default=Archetype.HUMANITIES, db_index=True)
    prompt_data = models.JSONField(default=dict, blank=True)
    selection_range = models.JSONField(default=dict, blank=True, null=True)
    reading_stimulus = models.TextField(blank=True, null=True)
    listening_transcript = models.TextField(blank=True, null=True)
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
        from .models import AssessmentSettings
        app_settings = AssessmentSettings.get_settings()
        if self.status == self.AssessmentStatus.COMPLETED:
            self.expiration_date = timezone.now() + timedelta(seconds=app_settings.assessment_expiration_seconds)
        elif self.status == self.AssessmentStatus.RESULTS_AVAILABLE:
            self.results_expiration_date = timezone.now() + timedelta(days=app_settings.results_expiration_days)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "1. Listado de Evaluaciones"
        ordering = ["-created_at"]

class Question(models.Model):
    class QuestionType(models.TextChoices):
        OPEN_ENDED = "open_ended", "Respuesta Abierta"
        MULTIPLE_CHOICE = "multiple_choice", "Opción Múltiple"
    class WidgetType(models.TextChoices):
        TEXT_AREA = "TEXT_AREA", "Área de Texto"
        AUDIO_RECORDER = "AUDIO_RECORDER", "Grabadora de Voz"
        RADIO_SELECT = "RADIO_SELECT", "Opción Múltiple"
        MATH_INPUT = "MATH_INPUT", "Editor Matemático"
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QuestionType.choices, default=QuestionType.OPEN_ENDED)
    widget_type = models.CharField(max_length=20, choices=WidgetType.choices, default=WidgetType.TEXT_AREA)
    model_answer = models.TextField()
    options = models.JSONField(default=list, blank=True)
    @property
    def requires_recording(self): return "[---RECORDING-REQUIRED---]" in self.question_text
    @property
    def requires_audio(self): return "[---AUDIO-REQUIRED---]" in self.question_text
    @property
    def transcript(self): return self.assessment.listening_transcript if self.requires_audio else None
    @property
    def display_text(self): return self.question_text.replace("[---RECORDING-REQUIRED---]", "").replace("[---AUDIO-REQUIRED---]", "").strip()
    class Meta:
        verbose_name = "Pregunta"
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
    def save(self, *args, **kwargs): self.pk = 1; super().save(*args, **kwargs)
    @classmethod
    def get_settings(cls): obj, _ = cls.objects.get_or_create(pk=1); return obj
    class Meta:
        verbose_name = "Ajuste de Motor"
        verbose_name_plural = "0. Configuración del Motor"
