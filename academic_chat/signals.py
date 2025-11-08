# /home/MiguelAeTxio/CampuStudiOnline/academic_chat/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import PendingEnrollment

logger = logging.getLogger(__name__)


@receiver(post_save, sender=get_user_model())
@transaction.atomic
def process_pending_enrollments(sender, instance, created, **kwargs):
    if created and instance.email:
        user_email = instance.email.lower()

        enrollments_to_process = PendingEnrollment.objects.filter(
            email__iexact=user_email
        )

        if not enrollments_to_process.exists():
            return

        logger.info(
            f"Nuevo usuario registrado con email '{user_email}'. Procesando {enrollments_to_process.count()} matrículas pendientes."
        )

        processed_count = 0
        for enrollment in enrollments_to_process:
            try:
                enrollment.academic_chat_link.enrolled_students.add(instance)
                enrollment.delete()
                processed_count += 1

            except Exception as e:
                logger.error(
                    f"Error al procesar la matrícula pendiente ID {enrollment.id} "
                    f"para el usuario '{instance.username}' en la sala '{enrollment.academic_chat_link.slug}': {e}",
                    exc_info=True,
                )

        logger.info(
            f"Se procesaron y eliminaron {processed_count} matrículas pendientes para el usuario '{instance.username}'."
        )
