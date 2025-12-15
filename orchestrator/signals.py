# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
import logging

from .models import ContentRequest
from .tasks import global_orchestrator_task

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ContentRequest)
def auto_approve_academic_requests(sender, instance, created, **kwargs):
    """
    Automatización Hito 24: Auto-aprobación de solicitudes de contenido académico.
    
    Cuando se crea una nueva ContentRequest (vinculada a una Asignatura/Subject),
    el sistema la pasa automáticamente a estado APPROVED para que el orquestador
    pueda procesarla sin intervención humana.
    
    Excluye explícitamente las solicitudes de contenido libre (FreeContentRequest),
    ya que son un modelo diferente.
    """
    if created and instance.status == ContentRequest.StatusChoices.PENDING:
        # Verificación: Asegurar que es una solicitud académica (tiene subject)
        if instance.subject:
            logger.info(
                f"AUTOMATION: Auto-aprobando solicitud académica para '{instance.subject.name}' (ID: {instance.id})."
            )
            
            # Actualizamos el estado de forma atómica usando update()
            # Esto evita disparar recursivamente el método save() y sus señales asociadas
            ContentRequest.objects.filter(pk=instance.pk).update(
                status=ContentRequest.StatusChoices.APPROVED
            )
            
            # Despertar al orquestador inmediatamente para atender la prioridad
            # Usamos on_commit para asegurar que la transacción de BD esté cerrada antes de que Celery la lea
            transaction.on_commit(lambda: global_orchestrator_task.delay())
