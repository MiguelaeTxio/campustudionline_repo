from celery import shared_task
from django.contrib.auth import get_user_model
import logging
from django.conf import settings
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.action_source import ActionSource
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.api import FacebookAdsApi
import time
from .models import MetaConversionEvent

task_logger = logging.getLogger("celery_tasks")

@shared_task
def cleanup_inactive_user(user_id):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        if not user.is_active:
            task_logger.info(f"Limpiando usuario inactivo: {user.username} (ID: {user_id}).")
            user.delete()
    except User.DoesNotExist:
        pass

def queue_meta_conversion_event(event_name, user_details, event_id=None, source_url=None, custom_data_params=None):
    """
    Sustituye a la antigua tarea asíncrona. Ahora guarda en BD para procesamiento en lote.
    """
    try:
        MetaConversionEvent.objects.create(
            event_name=event_name,
            user_details=user_details,
            event_id=event_id,
            source_url=source_url,
            custom_data_params=custom_data_params
        )
        return True
    except Exception as e:
        task_logger.error(f"Error al encolar evento Meta en BD: {str(e)}")
        return False

@shared_task
def process_meta_conversion_batch():
    """
    Tarea periódica que procesa los eventos pendientes en la BD.
    """
    pixel_id = getattr(settings, 'META_PIXEL_ID', None)
    access_token = getattr(settings, 'META_CONVERSIONS_API_TOKEN', None)
    
    if not pixel_id or not access_token:
        return

    events_to_process = MetaConversionEvent.objects.filter(processed=False)[:100]
    if not events_to_process:
        return

    try:
        FacebookAdsApi.init(access_token=access_token)
        meta_events = []
        
        for db_event in events_to_process:
            user_data = UserData(
                emails=[db_event.user_details.get('email_hash')],
                client_ip_address=db_event.user_details.get('client_ip_address'),
                client_user_agent=db_event.user_details.get('client_user_agent'),
                fbc=db_event.user_details.get('fbc'),
                fbp=db_event.user_details.get('fbp'),
            )

            custom_data = None
            if db_event.custom_data_params:
                custom_data = CustomData(**db_event.custom_data_params)

            event = Event(
                event_name=db_event.event_name,
                event_time=int(db_event.created_at.timestamp()),
                user_data=user_data,
                custom_data=custom_data,
                event_source_url=db_event.source_url,
                action_source=ActionSource.WEBSITE,
            )
            if db_event.event_id:
                event.event_id = db_event.event_id
            
            meta_events.append(event)

        event_request = EventRequest(events=meta_events, pixel_id=pixel_id)
        event_request.execute()
        
        # Marcar como procesados
        ids = [e.id for e in events_to_process]
        MetaConversionEvent.objects.filter(id__in=ids).update(processed=True)
        task_logger.info(f"Batch de Meta CAPI enviado con éxito: {len(meta_events)} eventos.")

    except Exception as e:
        task_logger.error(f"Error en batch Meta CAPI: {str(e)}")

# Mantener alias para compatibilidad con código existente que use delay()
@shared_task
def send_meta_conversion_event(*args, **kwargs):
    queue_meta_conversion_event(*args, **kwargs)
