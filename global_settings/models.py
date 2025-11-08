from django.db import models
from django.core.exceptions import ValidationError


class MaintenanceSettings(models.Model):
    maintenance_mode_active = models.BooleanField(
        default=False,
        verbose_name="Activar Modo Mantenimiento",
        help_text="Marcar para activar la página de mantenimiento para los usuarios. "
        "Los superusuarios y IPs permitidas seguirán teniendo acceso.",
    )
    # You can add a field for a custom message in the future if you want
    # custom_maintenance_message = models.TextField(
    #     blank=True,
    #     null=True,
    #     verbose_name="Mensaje de Mantenimiento Personalizado (Opcional)",
    #     help_text="Si se deja en blanco, se usará el mensaje por defecto de la plantilla."
    # )

    def __str__(self):
        status = "Activo" if self.maintenance_mode_active else "Inactivo"
        return f"Modo Mantenimiento ({status})"

    class Meta:
        verbose_name = "Configuración de Mantenimiento"
        verbose_name_plural = "Configuración de Mantenimiento"  # There should only be one

    def save(self, *args, **kwargs):
        # Ensure that only one instance exists (Singleton)
        if not self.pk and MaintenanceSettings.objects.exists():
            raise ValidationError(
                "Solo puede existir una instancia de MaintenanceSettings. Edita la existente."
            )
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        # Gets the single settings instance, or creates it if it doesn't exist.
        # We use a predictable ID (e.g., 1) for the single instance.
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={"maintenance_mode_active": False},  # Default value if created
        )
        return obj
