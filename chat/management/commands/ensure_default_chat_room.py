# chat/management/commands/ensure_default_chat_room.py
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from chat.models import ChatRoom, RoomMembership
import logging

logger = logging.getLogger(__name__)

DEFAULT_ROOM_NAME = "CampuStudiOnline"
DEFAULT_ROOM_SLUG = slugify(DEFAULT_ROOM_NAME)  # Debería ser 'campustudionline'


class Command(BaseCommand):
    help = _(
        "Ensures the default platform-wide chat room exists and is correctly configured."
    )

    def handle(self, *args, **options):
        self.stdout.write(
            f"[{settings.DEBUG}] DEBUG mode: {settings.DEBUG}", self.style.NOTICE
        )
        self.stdout.write(
            self.style.SUCCESS(
                _("Verificando existencia de la sala general de la plataforma...")
            )
        )
        logger.info("Comando ensure_default_chat_room iniciado.")

        try:
            # Usamos get_or_create para ser idempotentes.
            # Buscamos por slug o por el flag is_platform_default
            room, created = ChatRoom.objects.get_or_create(
                slug=DEFAULT_ROOM_SLUG,
                defaults={
                    "name": DEFAULT_ROOM_NAME,
                    "description": _(
                        "Sala general de chat de la plataforma CampuStudiOnline. Todos los usuarios activos son miembros."
                    ),
                    "is_private": False,  # La sala general debe ser pública
                    "is_platform_default": True,  # Marcarla explícitamente como la sala por defecto
                    # El creador puede ser None para una sala gestionada por la plataforma,
                    # o podrías asignar un superusuario si lo deseas.
                    # Por ahora, la dejamos sin creador asociado a un usuario específico.
                    "creator": None,
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        _(
                            f'Sala general "{DEFAULT_ROOM_NAME}" ({DEFAULT_ROOM_SLUG}) creada con éxito.'
                        )
                    )
                )
                logger.info(
                    f"Sala general '{DEFAULT_ROOM_NAME}' ({DEFAULT_ROOM_SLUG}) creada."
                )

            # Asegurarse de que los flags estén correctos incluso si ya existía con el slug pero no con el flag
            if not room.is_platform_default or room.is_private:
                room.is_platform_default = True
                room.is_private = False
                room.save(update_fields=["is_platform_default", "is_private"])
                self.stdout.write(
                    self.style.WARNING(
                        _(
                            f'Se actualizaron los flags de la sala general "{room.name}" ({room.slug}).'
                        )
                    )
                )
                logger.warning(
                    f"Actualizados flags is_platform_default/is_private para sala general '{room.name}'."
                )

            # Asegurarse de que todos los usuarios activos tengan membresía si no la tienen
            User = get_user_model()
            all_users = User.objects.filter(is_active=True)
            memberships_to_create = []
            # Usar una subconsulta eficiente o verificar la existencia de membresías
            # Opción 1: IDs de usuarios sin membresía activa en esta sala
            user_ids_with_membership = RoomMembership.objects.filter(
                room=room, status=RoomMembership.STATUS_MEMBER
            ).values_list("user_id", flat=True)
            user_ids_without_membership = (
                User.objects.filter(is_active=True)
                .exclude(id__in=user_ids_with_membership)
                .values_list("id", flat=True)
            )

            if user_ids_without_membership.exists():
                users_to_add_membership = User.objects.filter(
                    id__in=user_ids_without_membership
                )
                for user in users_to_add_membership:
                    # Crear membresía activa por defecto
                    memberships_to_create.append(
                        RoomMembership(
                            user=user,
                            room=room,
                            status=RoomMembership.STATUS_MEMBER,  # Son miembros por defecto
                            role=RoomMembership.ROLE_MEMBER,  # Rol por defecto
                        )
                    )
                if memberships_to_create:
                    RoomMembership.objects.bulk_create(memberships_to_create)
                    self.stdout.write(
                        self.style.SUCCESS(
                            _(
                                f'Creadas {len(memberships_to_create)} membresías por defecto para usuarios existentes sin membresía activa en la sala "{room.name}".'
                            )
                        )
                    )
                    logger.info(
                        f"Creadas {len(memberships_to_create)} membresías por defecto en sala '{room.name}' para usuarios sin membresía activa."
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        _(
                            "Todos los usuarios activos existentes ya tienen membresía activa en la sala general."
                        )
                    )
                )
                logger.info(
                    "Todos los usuarios activos existentes ya tienen membresía activa en la sala general."
                )

        except Exception as e:
            logger.critical(
                f"ERROR CRÍTICO al ejecutar ensure_default_chat_room: {e}",
                exc_info=True,
            )
            raise CommandError(
                _(f"Error al asegurar la existencia de la sala general: {e}")
            )

        self.stdout.write(
            self.style.SUCCESS(_("Comando ensure_default_chat_room finalizado."))
        )
        logger.info("Comando ensure_default_chat_room finalizado.")
