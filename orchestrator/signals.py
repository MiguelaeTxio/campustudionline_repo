from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
import logging

from .models import ContentRequest
from .tasks import global_orchestrator_task

logger = logging.getLogger(__name__)

def safe_orchestrator_trigger():
    """
    ARQUITECTURA DE AISLAMIENTO DE FALLOS:
    Intenta poner en cola la tarea del orquestador.
    Si el Broker (Redis) está saturado o caído, captura la excepción para
    evitar que la transacción de la Base de Datos (MySQL) se revierta.
    
    Esto prioriza la persistencia de los datos del usuario sobre la
    inmediatez del procesamiento en segundo plano.
    """
    try:
        global_orchestrator_task.delay()
    except Exception as e:
        # Registramos como CRITICAL porque requiere atención de infraestructura (Redis lleno)
        # pero permitimos que el flujo web continúe.
        logger.critical(f"INFRASTRUCTURE ALERT: No se pudo despertar al orquestador (Redis saturado). La solicitud se procesará en el siguiente ciclo programado. Error: {e}")

@receiver(post_save, sender=ContentRequest)
def auto_approve_academic_requests(sender, instance, created, **kwargs):
    """
    Automatización Hito 24: Auto-aprobación de solicitudes de contenido académico.
    """
    if created and instance.status == ContentRequest.StatusChoices.PENDING:
        # Verificación: Asegurar que es una solicitud académica (tiene subject)
        if instance.subject:
            logger.info(
                f"AUTOMATION: Auto-aprobando solicitud académica para '{instance.subject.name}' (ID: {instance.id})."
            )
            
            # Actualizamos el estado de forma atómica
            ContentRequest.objects.filter(pk=instance.pk).update(
                status=ContentRequest.StatusChoices.APPROVED
            )
            
            # CAMBIO ARQUITECTÓNICO: Usamos el dispatcher robusto en lugar de lambda
            transaction.on_commit(safe_orchestrator_trigger)
