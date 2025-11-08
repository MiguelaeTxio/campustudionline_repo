# /home/MiguelAeTxio/CampuStudiOnline/content_automation/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

from .models import ApiKey
from .tasks import automation_main_loop_task

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ApiKey)
def trigger_automation_on_key_availability(sender, instance, created, **kwargs):
    """
    Escucha los cambios en el modelo ApiKey para despertar proactivamente
    el bucle de automatización si una clave se vuelve disponible.
    """
    # Se activa si la clave está habilitada y no está en cuarentena.
    # Esto cubre tanto la creación de una nueva clave funcional como la
    # actualización de una existente (ej. sacarla de cuarentena manualmente).
    if instance.is_enabled and not instance.is_quarantined:
        logger.info(
            f"Señal detectada: La clave API '{instance.name}' está disponible. "
            "Intentando despertar el bucle principal de automatización."
        )
        # Llama a la tarea principal para que se ejecute lo antes posible.
        # La propia tarea comprobará el estado global y decidirá si debe
        # iniciar un nuevo trabajo.
        automation_main_loop_task.delay()
