# /home/MiguelAeTxio/CampuStudiOnline/delivery_note_processor/tasks.py
from celery import shared_task
import logging
from .models import DeliveryNote

logger = logging.getLogger(__name__)

@shared_task(
    name="process_delivery_note_image_task",
    queue='high_priority',
    routing_key='task.high_priority'
)
def process_delivery_note_image_task(delivery_note_id: int):
    """
    Tarea de Celery para procesar la imagen de un albarán de forma asíncrona.
    Ahora asignada a la cola de alta prioridad.
    """
    # La importación se mueve aquí para romper el ciclo de importación al arrancar Django.
    from . import services
    
    logger.info(f"CELERY TASK TRIGGERED: Iniciando procesamiento para el albarán ID: {delivery_note_id}")
    
    try:
        # La función de servicio ahora maneja todos los estados (éxito, error de IA, revisión).
        # Ya no es necesario cambiar el estado a 'processing' aquí.
        services.process_delivery_note_image(delivery_note_id)
        
        logger.info(f"CELERY TASK COMPLETED: La lógica de servicio para el albarán ID {delivery_note_id} ha finalizado.")
        
    except DeliveryNote.DoesNotExist:
        # Este caso es manejado por la función de servicio, pero lo mantenemos por si acaso.
        logger.error(f"La tarea de Celery no pudo encontrar el albarán con ID: {delivery_note_id}")
        
    except Exception as e:
        # Captura cualquier excepción no controlada dentro de `services` o a nivel de la tarea.
        logger.error(f"Error crítico en la tarea de Celery para el albarán ID {delivery_note_id}: {e}", exc_info=True)
        try:
            note_on_error = DeliveryNote.objects.get(id=delivery_note_id)
            note_on_error.status = 'error'
            note_on_error.processed_data = {'task_critical_error': str(e)}
            note_on_error.save()
        except DeliveryNote.DoesNotExist:
            logger.error(f"El albarán {delivery_note_id} no pudo ser encontrado para marcar el error crítico de la tarea.")


