# /home/MiguelAeTxio/CampuStudiOnline/messaging/management/commands/delete_chat_session.py

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from messaging.models import DirectChatSession
from django.db.models import Q
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    """
    Django management command to safely delete a direct chat session
    and all its associated messages between two specific users.
    """

    help = "Elimina la sesión de chat directo entre dos usuarios. Uso: delete_chat_session <username1> <username2>"

    def add_arguments(self, parser):
        """
        Adds the arguments that the command expects to receive.
        """
        parser.add_argument(
            "usernames",
            nargs=2,
            type=str,
            help="Los nombres de usuario de los dos participantes del chat.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """
        The main entry point for the management command.
        """
        username1, username2 = options["usernames"]

        if username1 == username2:
            raise CommandError(
                "Error: Debes proporcionar dos nombres de usuario diferentes."
            )

        self.stdout.write(
            self.style.NOTICE(
                f'>>> Iniciando la búsqueda y destrucción de la sesión de chat entre "{username1}" y "{username2}"...'
            )
        )

        try:
            user1 = User.objects.get(username=username1)
            user2 = User.objects.get(username=username2)
        except User.DoesNotExist:
            raise CommandError(
                f"Error: Uno o ambos usuarios no existen en la base de datos."
            )

        # We search for the session regardless of the order of the users
        session_to_delete = DirectChatSession.objects.filter(
            (Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1))
        )

        if not session_to_delete.exists():
            self.stdout.write(
                self.style.SUCCESS(
                    f'--- No se encontró ninguna sesión de chat activa entre "{username1}" y "{username2}". No se requiere ninguna acción.'
                )
            )
            return

        # Since there is a foreign key from DirectMessage to DirectChatSession
        # with on_delete=models.CASCADE, deleting the session will delete all its messages.
        try:
            num_sessions, deleted_details = session_to_delete.delete()
            num_messages = deleted_details.get("messaging.DirectMessage", 0)

            self.stdout.write(self.style.SUCCESS(f"\n>>> ¡DESTRUCCIÓN COMPLETADA!"))
            self.stdout.write(
                self.style.WARNING(
                    f"  - Se ha eliminado {num_sessions} sesión de chat."
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    f"  - Se han eliminado {num_messages} mensajes asociados a esa sesión."
                )
            )

        except Exception as e:
            raise CommandError(f"Error inesperado durante la eliminación: {e}")
