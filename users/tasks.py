# /users/tasks.py
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'.
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'.

from celery import shared_task
from django.contrib.auth import get_user_model
import logging
from django.conf import settings
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.api import FacebookAdsApi
import time


# Opcional: Configurar un logger específico para las tareas si quieres seguir su ejecución
task_logger = logging.getLogger("celery_tasks")


@shared_task
def cleanup_inactive_user(user_id):
    """
    Busca un usuario por su ID y lo elimina si todavía está inactivo.
    Se programa para ejecutarse X minutos después del registro.
    """
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        if not user.is_active:
            task_logger.info(
                f"Limpiando usuario inactivo: {user.username} (ID: {user_id}). La cuenta será eliminada."
            )
            user.delete()
        else:
            task_logger.info(
                f"El usuario {user.username} (ID: {user_id}) ya está activo. No se requiere limpieza."
            )
    except User.DoesNotExist:
        task_logger.warning(
            f"Se intentó limpiar el usuario con ID {user_id}, pero ya no existía. Posiblemente activado y luego eliminado, o nunca existió."
        )


@shared_task
def send_meta_conversion_event(event_name, user_details, event_id=None, source_url=None, custom_data_params=None):
    """
    Envía un evento a la API de Conversiones de Meta (CAPI).
    
    Args:
        event_name (str): Nombre del evento estándar (ej: 'CompleteRegistration', 'Purchase').
        user_details (dict): Diccionario con datos del usuario hash (em, ph) o crudos (client_ip_address, client_user_agent).
                             Claves esperadas: 'email_hash', 'client_ip_address', 'client_user_agent'.
        event_id (str): ID único para deduplicación (opcional pero recomendado).
        source_url (str): URL donde ocurrió el evento.
        custom_data_params (dict): Diccionario con parámetros para CustomData (content_ids, content_name, value, currency, etc.).
    """
    
    pixel_id = getattr(settings, 'META_PIXEL_ID', None)
    access_token = getattr(settings, 'META_CONVERSIONS_API_TOKEN', None)
    
    if not pixel_id or not access_token:
        task_logger.warning("Meta CAPI: Pixel ID or Access Token not configured. Skipping event.")
        return

    try:
        FacebookAdsApi.init(access_token=access_token)
        
        user_data = UserData(
            emails=[user_details.get('email_hash')],
            client_ip_address=user_details.get('client_ip_address'),
            client_user_agent=user_details.get('client_user_agent'),
            fbc=user_details.get('fbc'),
            fbp=user_details.get('fbp'),
        )

        custom_data = None
        if custom_data_params:
            custom_data = CustomData(
                content_ids=custom_data_params.get('content_ids'),
                content_name=custom_data_params.get('content_name'),
                content_category=custom_data_params.get('content_category'),
                content_type=custom_data_params.get('content_type'),
                value=custom_data_params.get('value'),
                currency=custom_data_params.get('currency'),
                num_items=custom_data_params.get('num_items'),
                order_id=custom_data_params.get('order_id'),
                status=custom_data_params.get('status'),
            )

        event = Event(
            event_name=event_name,
            event_time=int(time.time()),
            user_data=user_data,
            custom_data=custom_data,
            event_source_url=source_url,
            action_source=Event.ActionSource.WEBSITE,
        )
        
        if event_id:
            event.event_id = event_id

        events = [event]

        event_request = EventRequest(
            events=events,
            pixel_id=pixel_id,
        )

        event_response = event_request.execute()
        task_logger.info(f"Meta CAPI Event '{event_name}' sent successfully: {event_response}")

    except Exception as e:
        task_logger.error(f"Meta CAPI Error sending '{event_name}': {str(e)}")
