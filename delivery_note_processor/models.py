# /home/MiguelAeTxio/CampuStudiOnline/delivery_note_processor/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from orchestrator.models import ApiKey

class Vehicle(models.Model):
    """
    Representa un vehículo en la flota al que se pueden asociar albaranes.
    """
    vehicle_type = models.CharField(
        _("Tipo de Vehículo"),
        max_length=100,
        help_text=_("Ej: Furgoneta, Camión, Coche de servicio")
    )
    code = models.CharField(
        _("Código"),
        max_length=10,
        unique=True,
        help_text=_("Código único del vehículo en formato LetraNumeroNumero, ej: A01")
    )
    license_plate = models.CharField(
        _("Matrícula"),
        max_length=20,
        unique=True
    )

    class Meta:
        verbose_name = _("Vehículo")
        verbose_name_plural = _("Vehículos")
        ordering = ['code']

    def __str__(self):
        return f"{self.code} ({self.license_plate})"


class DeliveryNote(models.Model):
    """
    Representa un albarán subido y procesado, asociado a un vehículo.
    """
    STATUS_CHOICES = [
        ('pending', _('Pendiente')),
        ('processing', _('Procesando')),
        ('completed', _('Completado')),
        ('needs_review', _('Necesita Revisión')),
        ('error', _('Error de Procesamiento')),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Vehículo Asociado")
    )
    api_key_used = models.ForeignKey(
        ApiKey,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Clave de API Utilizada")
    )
    extracted_vehicle_code = models.CharField(
        _("Código de Vehículo Extraído"),
        max_length=50,
        null=True,
        blank=True,
        help_text=_("El código de vehículo exacto extraído por la IA, exista o no en la BBDD.")
    )
    original_image = models.ImageField(
        _("Imagen Original del Albarán"),
        upload_to='delivery_notes/%Y/%m/%d/'
    )
    processed_data = models.JSONField(
        _("Datos Procesados del Albarán"),
        null=True,
        blank=True,
        help_text=_("Contiene toda la información extraída del albarán en formato JSON.")
    )
    status = models.CharField(
        _("Estado"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    uploaded_at = models.DateTimeField(
        _("Fecha de Subida"),
        auto_now_add=True
    )
    processed_at = models.DateTimeField(
        _("Fecha de Procesamiento"),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("Albarán")
        verbose_name_plural = _("Albaranes")
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Albarán ID: {self.id} ({self.get_status_display()})"
