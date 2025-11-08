# /home/MiguelAeTxio/CampuStudiOnline/academic_chat/tasks.py
from celery import shared_task
from django.conf import settings
import logging

from .models import AcademicChatLink, AcademicChatMessage

logger = logging.getLogger(__name__)


@shared_task
def process_academic_chat_message(academic_link_id: str, sender_id: int, content: str):
    try:
        chat_link = AcademicChatLink.objects.get(id=academic_link_id)
        sender = settings.AUTH_USER_MODEL.objects.get(id=sender_id)

        AcademicChatMessage.objects.create(
            chat_link=chat_link,
            sender=sender,
            sender_username_display=sender.username,
            content=content,
        )
        logger.info(
            f"Tarea Celery: Mensaje de '{sender.username}' guardado en la sala académica "
            f"'{chat_link.slug}' (ID: {chat_link.id})."
        )
        return f"Mensaje para la sala {academic_link_id} procesado con éxito."

    except AcademicChatLink.DoesNotExist:
        logger.error(
            f"Tarea Celery: No se encontró AcademicChatLink con ID {academic_link_id}."
        )
        return f"Error: No se encontró el vínculo de chat con ID {academic_link_id}."
    except settings.AUTH_USER_MODEL.DoesNotExist:
        logger.error(
            f"Tarea Celery: No se encontró el usuario remitente con ID {sender_id}."
        )
        return f"Error: No se encontró el usuario remitente con ID {sender_id}."
    except Exception as e:
        logger.error(
            f"Tarea Celery: Error inesperado al procesar mensaje para sala {academic_link_id}. "
            f"Error: {e}",
            exc_info=True,
        )
        raise
