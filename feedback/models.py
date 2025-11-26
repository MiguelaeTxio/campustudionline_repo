import uuid
from django.db import models
from django.conf import settings
from contents.models import ContentMaterial

class FeedbackReport(models.Model):
    TYPE_CONTENT_ERROR = 'content_error'
    TYPE_SUGGESTION = 'suggestion'
    TYPE_TECHNICAL = 'technical'
    
    TYPE_CHOICES = [
        (TYPE_CONTENT_ERROR, 'Error en Contenido'),
        (TYPE_SUGGESTION, 'Sugerencia de Mejora'),
        (TYPE_TECHNICAL, 'Problema Técnico'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_IN_PROGRESS, 'En Progreso'),
        (STATUS_RESOLVED, 'Resuelto'),
        (STATUS_REJECTED, 'Descartado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_reports', verbose_name="Usuario")
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_SUGGESTION, verbose_name="Tipo de Reporte")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name="Estado")
    
    # Vinculación opcional con contenido específico
    content_material = models.ForeignKey(
        ContentMaterial, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reports',
        verbose_name="Contenido Relacionado"
    )
    
    title = models.CharField(max_length=200, verbose_name="Asunto")
    description = models.TextField(verbose_name="Descripción detallada")
    
    # Campos de gestión interna
    admin_response = models.TextField(blank=True, verbose_name="Respuesta del Administrador")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Reporte de Feedback"
        verbose_name_plural = "Reportes de Feedback"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_report_type_display()}] {self.title} - {self.user.username}"
