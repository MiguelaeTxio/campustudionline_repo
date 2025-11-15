# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/models.py
from django.db import models
from django.core.exceptions import ValidationError
from datetime import time, date

# Importaciones necesarias para las ForeignKeys en AutomationSettings
from academic_structure.models import Branch, Degree


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
