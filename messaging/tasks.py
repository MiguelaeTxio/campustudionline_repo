# /home/MiguelAeTxio/CampuStudiOnline/messaging/tasks.py
import logging
from celery import shared_task
from django.contrib.auth import get_user_model
from django.urls import reverse
from .push_utils import send_notification_to_user

User = get_user_model()
logger = logging.getLogger(__name__)


@shared_task(name="messaging.send_push_notification_for_message")
def send_push_notification_task(recipient_id, sender_username, encrypted_payload):
    """
    Celery task to send a push notification for a new message.
    """
    try:
        recipient = User.objects.get(id=recipient_id)
        logger.info(
            f"Celery Task: Initiating notification dispatch to {recipient.username} for a message from {sender_username}."
        )

        # Build the URL to the conversation
        conversation_url = reverse(
            "messaging:conversation_detail", kwargs={"username": sender_username}
        )

        send_notification_to_user(
            user=recipient,
            title=f"New message from {sender_username}",
            body="Click to view the message.",  # The actual body will be decrypted in the Service Worker
            url=conversation_url,
            encrypted_message_payload=encrypted_payload,
        )
        logger.info(
            f"Celery Task: send_notification_to_user called successfully for {recipient.username}."
        )
        return f"Notification sent to {recipient.username}"

    except User.DoesNotExist:
        logger.error(
            f"Celery Task: Could not find user with ID {recipient_id}."
        )
        return f"Error: User with ID {recipient_id} not found."
    except Exception as e:
        logger.error(
            f"Celery Task: An unexpected error occurred while sending notification for user ID {recipient_id}. Error: {e}",
            exc_info=True,
        )
        # Re-raise the exception so Celery can register it as a task failure
        raise
