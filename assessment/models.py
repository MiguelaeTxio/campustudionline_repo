# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Assessment(models.Model):
    """
    Represents a single AI-generated assessment session for a piece of content.
    """

    class AssessmentStatus(models.TextChoices):
        # Flujo de Generación
        PENDING = "PENDING", "Pendiente de Generación"
        PROCESSING = "PROCESSING", "Generando Cuestionario"
        COMPLETED = "COMPLETED", "Listo para Realizar"
        
        # Flujo de Corrección
        AWAITING_CORRECTION = "AWAITING_CORRECTION", "Pendiente de Corrección" # Estado intermedio
        CORRECTING = "CORRECTING", "Corrigiendo"
        RESULTS_AVAILABLE = "RESULTS_AVAILABLE", "Resultados Disponibles"

        # Estados de Expiración
        EXPIRED_UNTAKEN = "EXPIRED_UNTAKEN", "Expirado (No Realizado)"
        CORRECTION_EXPIRED = "CORRECTION_EXPIRED", "Corrección Expirada"
        
        # Estado de Fallo Consolidado
        FAILED_FATAL = "FAILED_FATAL", "Fallo Permanente"

        # Estado Final de Usuario
        USER_CANCELLED = "USER_CANCELLED", "Cancelado por el Usuario"

    content_copy = models.ForeignKey(
        "contents.ContentCopy",
        on_delete=models.CASCADE,
        related_name="assessments",
        verbose_name="Copia de Estudio",
        null=False,
        help_text="La copia de estudio específica a la que está vinculada esta evaluación."
    )
    content = models.ForeignKey(
        "contents.ContentMaterial",
        on_delete=models.CASCADE,
        related_name="assessments",
        verbose_name="Contenido Original",
        editable=False,
        help_text="Se rellena automáticamente desde la Copia de Estudio."
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assessments",
        verbose_name="Usuario",
    )
    status = models.CharField(
        max_length=50,
        choices=AssessmentStatus.choices,
        default=AssessmentStatus.PENDING,
        verbose_name="Estado",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Creación"
    )

    total_questions_expected = models.PositiveIntegerField(
        default=0,
        verbose_name="Total de preguntas esperadas",
        help_text=_(
            "The total number of sections detected that will be converted into questions."
        ),
    )
    questions_processed = models.PositiveIntegerField(
        default=0,
        verbose_name="Preguntas procesadas",
        help_text=_("The number of questions that the worker has already generated."),
    )

    was_viewed = models.BooleanField(
        default=False,
        verbose_name="Corrección Vista",
        help_text=_(
            "Indicates if the user has viewed the results of this correction to avoid penalization."
        ),
    )

    expiration_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Fecha de Caducidad para Realizar"),
        help_text=_("La evaluación debe realizarse antes de esta fecha."),
    )
    results_expiration_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Fecha de Caducidad de Resultados"),
        help_text=_("Los resultados de la evaluación estarán disponibles hasta esta fecha."),
    )

    last_error = models.TextField(
        blank=True, null=True, verbose_name=_("Último Error Registrado")
    )
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para:
        1. Asegurar que el 'content' original siempre se deriva de la 'content_copy'.
        2. Establecer las fechas de caducidad basándose en el estado.
        """
        # 1. Enlace forzado a ContentMaterial a través de ContentCopy
        if self.content_copy and not self.content_id:
            self.content = self.content_copy.original_content

        # 2. Lógica de fechas de caducidad
        app_settings = AssessmentSettings.get_settings()
        if self.status == self.AssessmentStatus.COMPLETED:
            self.expiration_date = timezone.now() + timedelta(
                seconds=app_settings.assessment_expiration_seconds
            )
            self.results_expiration_date = None
        elif self.status == self.AssessmentStatus.RESULTS_AVAILABLE:
            self.results_expiration_date = timezone.now() + timedelta(
                days=app_settings.results_expiration_days
            )
            self.expiration_date = None
        else:
            self.expiration_date = None
            self.results_expiration_date = None

        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        ordering = ["-created_at"]

    def __str__(self):
        # Usamos content_copy para la representación para reforzar la nueva lógica
        return (
            f"Assessment for copy of '{self.content_copy.original_content.title}' "
            f"by {self.user.username} ({self.get_status_display()})"
        )


class Question(models.Model):
    """
    Stores an individual question within an assessment.
    """



    class QuestionType(models.TextChoices):
        OPEN_ENDED = "open_ended", "Respuesta Abierta"
        MULTIPLE_CHOICE = "multiple_choice", "Opción Múltiple"

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Evaluación",
    )
    question_text = models.TextField(verbose_name="Texto de la Pregunta")
    question_type = models.CharField(
        max_length=20,
        choices=QuestionType.choices,
        default=QuestionType.OPEN_ENDED,
        verbose_name="Tipo de Pregunta",
    )
    model_answer = models.TextField(
        verbose_name="Respuesta Modelo (Generada por IA)",
        help_text=_(
            "The ideal answer that will be used as a reference for correction."
        ),
    )

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        ordering = ["assessment", "id"]

    def __str__(self):
        return self.question_text[:80]


class UserAnswer(models.Model):
    """
    Stores a user's answer to an open-ended question.
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="user_answers",
        verbose_name="Pregunta",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_answers",
        verbose_name="Usuario",
    )
    answer_text = models.TextField(verbose_name="Texto de la Respuesta del Usuario")
    answered_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Respondido En"
    )
    score = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Puntuación",
        help_text=_("The assigned score, e.g., from 0.0 to 10.0."),
    )
    feedback = models.TextField(
        blank=True,
        verbose_name="Comentarios",
        help_text=_("Comments or corrections generated by the AI."),
    )
    correction_expiration_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de Expiración de la Corrección"
    )

    class Meta:
        verbose_name = "Respuesta del Usuario"
        verbose_name_plural = "Respuestas del Usuario"
        ordering = ["-answered_at"]

    def __str__(self):
        return f"Answer from {self.user.username} for question {self.question.id}"


class AssessmentSettings(models.Model):
    """
    Singleton model to hold sitewide settings for the assessment application.
    """

    daily_limit = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Límite Diario de Evaluaciones por Usuario"),
        help_text=_(
            "Número máximo de evaluaciones que un usuario puede generar en 24 horas."
        ),
    )
    weekly_limit = models.PositiveIntegerField(
        default=3,
        verbose_name=_("Límite Semanal de Evaluaciones por Usuario"),
        help_text=_(
            "Número máximo de evaluaciones que un usuario puede generar en 7 días."
        ),
    )
    assessment_expiration_seconds = models.PositiveIntegerField(
        default=86400,  # 24 hours
        verbose_name=_("Tiempo para Realizar una Evaluación (segundos)"),
        help_text=_(
            "Tiempo máximo que un usuario tiene para completar una evaluación desde que está disponible."
        ),
    )
    results_expiration_days = models.PositiveIntegerField(
        default=7,
        verbose_name=_("Tiempo de Visibilidad de Resultados (días)"),
        help_text=_(
            "Número de días que los resultados de una evaluación permanecen visibles."
        ),
    )

    class Meta:
        verbose_name = _("Configuración de Evaluaciones")
        verbose_name_plural = _("Configuraciones de Evaluaciones")

    def __str__(self):
        return str(_("Configuración de Evaluaciones"))

    def save(self, *args, **kwargs):
        """
        Forces the singleton pattern by ensuring that this object is always
        saved to the database with a primary key (pk) of 1.
        """
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
