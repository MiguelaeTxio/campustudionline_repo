# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/models.py
import uuid
from datetime import time, date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

# Importaciones necesarias para las ForeignKeys y modelos movidos
from academic_structure.models import Branch, Degree, TimeStampedModel


class ApiKey(models.Model):
    """Almacena una única clave de API para el servicio de Gemini."""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre Identificativo",
        help_text="Ej: 'Clave Primaria', 'Clave de Backup 1'"
    )
    key = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Clave de API",
        help_text="La clave de API de Google Gemini."
    )
    is_enabled = models.BooleanField(
        default=True,
        verbose_name="¿Habilitada?",
        help_text="Desmarcar para excluir esta clave de la rotación automática."
    )
    is_quarantined = models.BooleanField(
        default=False,
        verbose_name="En Cuarentena por Límite de Cuota",
        help_text="Marcado si la clave falla persistentemente. Una tarea diaria la liberará."
    )
    consecutive_failures = models.PositiveIntegerField(
        default=0,
        verbose_name="Fallos Consecutivos",
        help_text="Contador de errores de cuota (ResourceExhausted) para gestionar la cuarentena."
    )
    

    def __str__(self):
        return "Configuración Maestra del Sistema"

    class Meta:
        verbose_name = "Clave de API de Gemini"
        verbose_name_plural = "B. Claves de API de Gemini"
        ordering = ['id']

    def __str__(self):
        return self.name


class AutomationSettings(models.Model):
    """
    Modelo Singleton para almacenar el estado global del sistema de automatización.
    """
    is_running = models.BooleanField(
        default=False,
        verbose_name="Interruptor Maestro de Automatización",
        help_text="Si está activado, la tarea 'always-on' buscará y procesará tareas pendientes."
    )
    quarantine_reset_time = models.TimeField(
        default=time(9, 5),
        verbose_name="Hora de Reseteo de Cuarentena",
        help_text="La hora (en zona horaria del servidor) a la que se liberarán las claves en cuarentena."
    )
    last_quarantine_reset_date = models.DateField(
        default=date(2000, 1, 1),
        verbose_name="Fecha del Último Reseteo de Cuarentena",
        help_text="Registra el último día que se ejecutó el reseteo para asegurar que solo ocurra una vez al día."
    )
    active_api_key = models.ForeignKey(
        ApiKey,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name="Clave de API Activa",
        help_text="La clave que el sistema está utilizando actualmente para las generaciones."
    )
    seed_branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Rama Semilla",
        help_text="La rama académica seleccionada como punto de partida para la generación."
    )
    seed_degree = models.ForeignKey(
        Degree,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Grado Semilla",
        help_text="El grado académico seleccionado como punto de partida."
    )
    seed_year = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Año Académico Semilla",
        help_text="El año académico específico (ej. 'Primero', 'Segundo') para acotar la generación."
    )
    last_run_timestamp = models.DateTimeField(
        null=True, blank=True, verbose_name="Última Ejecución"
    )
    last_run_status = models.TextField(
        blank=True, verbose_name="Estado del Último Ciclo"
    )

    # ==========================================================================
    # HITO 24: PARÁMETROS DE RESILIENCIA CONFIGURABLES
    # ==========================================================================
    max_task_actuations = models.PositiveIntegerField(
        default=20,
        verbose_name="Umbral de Actuaciones Máximas por Tarea",
        help_text="(Fusible Global) Número máximo de veces que el orquestador intentará iniciar una misma tarea antes de marcarla como fallo fatal."
    )
    max_consecutive_api_errors = models.PositiveIntegerField(
        default=4,
        verbose_name="Umbral de Errores de API Consecutivos",
        help_text="(Fusible de Cuota) Número de fallos de API seguidos en una misma sección antes de poner la clave en cuarentena."
    )
    zombie_task_threshold_hours = models.PositiveIntegerField(
        default=24,
        verbose_name="Umbral de Horas para Tareas Zombie",
        help_text="Número de horas de inactividad para que una tarea 'procesando' sea considerada zombie y purgada."
    )

    event_log = models.JSONField(
        default=list, blank=True, verbose_name="Historial de Eventos del Motor"
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and AutomationSettings.objects.exists():
            raise ValidationError('Solo puede existir una instancia de AutomationSettings.')
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Método de conveniencia para obtener la única instancia de configuración, forzando un fetch fresco."""
        try:
            obj = cls.objects.get(pk=1)
        except cls.DoesNotExist:
            obj = cls.objects.create(pk=1, seed_year="")
        
        obj.refresh_from_db()
        return obj

    class Meta:
        verbose_name = "Configuración del Centro de Control de Contenidos"
        verbose_name_plural = "C. Configuración del Centro de Control de Contenidos"


# ==============================================================================
# INICIO DE MODELOS MOVIDOS DESDE 'content_automation'
# ==============================================================================

class ContentRequest(TimeStampedModel):
    """
    Representa el "tema" de una solicitud de contenido para una única asignatura.
    Agrupa a todos los usuarios que han solicitado este contenido.
    """
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pendiente de Aprobación"
        APPROVED = "APPROVED", "Aprobada para Automatización"
        IN_PROGRESS = "IN_PROGRESS", "Generación en Proceso"
        FULFILLED = "FULFILLED", "Satisfecha"
        REJECTED = "REJECTED", "Rechazada"

    subject = models.OneToOneField(
        'academic_structure.Subject',
        on_delete=models.CASCADE,
        related_name="content_request",
        verbose_name="Asignatura Solicitada"
    )

    requesters = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="content_requests",
        verbose_name="Usuarios Solicitantes"
    )

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="Estado de la Solicitud"
    )

    class Meta:
        verbose_name = "Solicitud de Contenido"
        verbose_name_plural = "Solicitudes de Contenido"
        ordering = ["-created_at"]

    @property
    def request_count(self):
        """Propiedad dinámica que calcula el número de solicitantes."""
        return self.requesters.count()

    def __str__(self):
        return f"Solicitud para {self.subject.name} ({self.request_count} peticiones)"


class PendingContentTask(TimeStampedModel):
    """
    [V5] Gestiona las tareas de creación de contenido y almacena metadatos para estadísticas.
    Este modelo es el monitor de estado y la fuente de verdad para el historial de generación.
    """

    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        PROCESSING = "PROCESSING", "Procesando"
        COMPLETED = "COMPLETED", "Completada"
        FAILED = "FAILED", "Fallida (Manual)"
        FAILED_RETRYABLE = "FAILED_RETRYABLE", "Fallida (Reintentable)"
        FAILED_QUOTA = "FAILED_QUOTA", "Fallida (Límite de Cuota)"
        FAILED_FATAL = "FAILED_FATAL", "Fallida (Fatal)"
        PAUSED = "PAUSED", "Pausado por el Administrador"

    class TaskOrigin(models.TextChoices):
        MASS_GENERATION = "MASS_GENERATION", "Masivo"
        APPROVED_REQUEST = "APPROVED_REQUEST", "Solicitud Aprobada"
        MANUAL_CREATION = "MANUAL_CREATION", "Creación Manual"
        SYSTEM_RESTART = "SYSTEM_RESTART", "Reinicio por Fallo"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    subject = models.ForeignKey(
        'academic_structure.Subject',
        on_delete=models.CASCADE,
        related_name="content_tasks",
        verbose_name="Asignatura (Curso Académico)",
        null=True,
        blank=True,
        help_text="Asignar solo si es un curso derivado de una asignatura académica.",
    )
    course_title = models.CharField(
        max_length=255,
        verbose_name="Título del Curso (Curso Libre)",
        blank=True,
        help_text="Proporcionar solo si es un curso libre.",
    )
    prompt_text = models.TextField(
        verbose_name="Descripción/Prompt (Curso Libre)",
        blank=True,
        help_text="Descripción detallada o prompt para generar un curso libre.",
    )

    status = models.CharField(
        max_length=30,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="Estado",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_content_tasks",
        verbose_name="Asignado a",
    )
    content_material = models.OneToOneField(
        "contents.ContentMaterial",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="source_task",
        verbose_name="Material de Contenido Resultante",
    )

    task_origin = models.CharField(
        max_length=30,
        choices=TaskOrigin.choices,
        default=TaskOrigin.MANUAL_CREATION,
        verbose_name="Origen de la Tarea"
    )
    api_key_used = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Clave de API Utilizada"
    )
    section_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Número de Secciones"
    )

    structured_content = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        verbose_name="Contenido Estructurado (JSON)",
        help_text="Almacena artefactos intermedios como el temario o las secciones generadas.",
    )
    notes = models.TextField(blank=True, verbose_name="Notas adicionales")
    log_file_path = models.CharField(max_length=512, verbose_name="Ruta al Archivo de Log", null=True, blank=True, help_text="Ruta al archivo de log detallado de la tarea.")
    task_log = models.JSONField(
        "Log de Tarea",
        default=list,
        blank=True,
        help_text="Registro de eventos y pasos de la tarea.",
    )
    last_error = models.TextField(
        blank=True, null=True, verbose_name="Último Error Fatal"
    )

    # ==========================================================================
    # CAMPOS DE RESILIENCIA Y CONTROL DE EJECUCIÓN (HITO 24)
    # ==========================================================================
    global_actuation_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Contador Global de Actuaciones",
        help_text="Fusible físico. Cuenta las veces que el orquestador ha intentado procesar esta tarea. Si supera el límite, se aborta."
    )
    consecutive_api_errors = models.PositiveIntegerField(
        default=0,
        verbose_name="Errores Consecutivos de API",
        help_text="Contador de fallos seguidos en llamadas a la API. Se usa para la lógica de reintento exponencial o aborto."
    )
    last_api_error_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Momento del Último Error de API",
        help_text='Timestamp del último fallo de API para calcular ventanas de "amnistía".'
    )
    last_error_api_key = models.ForeignKey(
        ApiKey,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="failed_tasks",
        verbose_name="Última Clave de API Fallida",
        help_text="La clave que provocó el último error, para evitar culpar a nuevas claves."
    )
    current_step = models.PositiveIntegerField(
        default=0,
        verbose_name="Paso Actual de Ejecución",
        help_text="Puntero para reanudar la generación en el punto exacto (ej: índice del temario)."
    )
    last_heartbeat = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Último Latido (Heartbeat)",
        help_text='Marca de tiempo para detectar tareas "zombies" que murieron silenciosamente.'
    )

    class Meta:
        verbose_name = "Tarea de Automatización de Contenido"
        verbose_name_plural = "Tareas de Automatización de Contenido"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["subject"],
                condition=~Q(status__in=["COMPLETED", "FAILED", "FAILED_FATAL"])
                & Q(subject__isnull=False),
                name="unique_active_academic_task_per_subject",
            ),
            models.UniqueConstraint(
                fields=["course_title"],
                condition=~Q(status__in=["COMPLETED", "FAILED", "FAILED_FATAL"])
                & Q(subject__isnull=True),
                name="unique_active_free_task_per_title",
            ),
            models.CheckConstraint(
                check=(
                    Q(subject__isnull=False)
                    & Q(course_title__exact="")
                    & Q(prompt_text__exact="")
                    | Q(subject__isnull=True)
                    & ~Q(course_title__exact="")
                    & ~Q(prompt_text__exact="")
                ),
                name="task_type_is_exclusive",
            ),
        ]

    def __str__(self):
        title = self.subject.name if self.subject else self.course_title
        return f"Tarea para '{title}' ({self.get_status_display()})"

    @staticmethod
    def has_active_task(subject):
        return (
            PendingContentTask.objects.filter(subject=subject)
            .exclude(
                status__in=[
                    PendingContentTask.StatusChoices.COMPLETED,
                    PendingContentTask.StatusChoices.FAILED,
                    PendingContentTask.StatusChoices.FAILED_FATAL,
                ]
            )
            .exists()
        )


class GeneratedContentChunk(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(
        PendingContentTask,
        on_delete=models.CASCADE,
        related_name="content_chunks",
        verbose_name="Tarea Asociada",
    )
    order = models.PositiveIntegerField(
        verbose_name="Orden de Sección",
        help_text="El número de orden para reconstruir el documento final.",
    )
    content = models.TextField(
        verbose_name="Contenido de la Sección",
        help_text="El texto generado por la IA para esta sección.",
    )
    is_processed = models.BooleanField(
        default=False,
        verbose_name="¿Procesado e incluido?",
        help_text="Indica si este fragmento ya ha sido incluido en el ContenidoMaterial final.",
    )
    ai_sources = models.TextField(
        blank=True, null=True, verbose_name="Fuentes de la IA"
    )

    class Meta:
        verbose_name = "Fragmento de Contenido Generado"
        verbose_name_plural = "Fragmentos de Contenido Generado"
        ordering = ["task", "order"]
        unique_together = ("task", "order")

    def __str__(self):
        return f"Fragmento {self.order} para la tarea {self.task.id}"


class FreeContentRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_APPROVED, 'Aprobada'),
        (STATUS_REJECTED, 'Rechazada'),
    ]

    REASON_SIMILAR_EXISTS = 'similar_exists'
    REASON_ETHICS_VIOLATION = 'ethics_violation'
    REASON_OFFENSIVE_CONTENT = 'offensive_content'
    REASON_OTHER = 'other'
    REJECTION_CHOICES = [
        (REASON_SIMILAR_EXISTS, 'Contenido Similar Existente'),
        (REASON_ETHICS_VIOLATION, 'Incumplimiento del Código Ético'),
        (REASON_OFFENSIVE_CONTENT, 'Contenido de Carácter Ofensivo'),
        (REASON_OTHER, 'Otro (ver notas)'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="free_content_requests", verbose_name="Usuario Solicitante"
    )
    title = models.CharField(
        max_length=255, verbose_name="Título del Curso"
    )
    detailed_prompt = models.TextField(
        verbose_name="Descripción Detallada / Prompt"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING,
        verbose_name="Estado de la Solicitud"
    )
    
    rejection_reason = models.CharField(
        max_length=30, choices=REJECTION_CHOICES, blank=True, null=True,
        verbose_name="Motivo del Rechazo",
        help_text="Visible solo si el estado es 'Rechazada'."
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Solicitud de Contenido Libre"
        verbose_name_plural = "A. Solicitudes de Contenido Libre"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Solicitud Libre de '{self.title}' por {self.requester.username} ({self.get_status_display()})"
