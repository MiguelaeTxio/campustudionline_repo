# /home/MiguelAeTxio/CampuStudiOnline/messaging/management/commands/purge_test_data.py

from django.core.management.base import BaseCommand
from django.db import transaction

# FIX: Use the correct model names
from messaging.models import DirectChatSession, DirectMessage
from users.models import PerfilUsuario


class Command(BaseCommand):
    """
    Django management command to purge all test data from the messaging application
    and clear cryptographic keys from user profiles.
    """

    help = "Elimina todos los chats, mensajes y resetea las claves criptográficas y sales de todos los usuarios."

    def handle(self, *args, **options):
        """
        The main entry point for the management command.
        """
        self.stdout.write(
            self.style.WARNING(">>> Iniciando la purga de datos de prueba...")
        )

        try:
            with transaction.atomic():
                # 1. Delete all direct messages
                # FIX: Use DirectMessage
                num_messages, _ = DirectMessage.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"--- {num_messages} mensajes eliminados con éxito."
                    )
                )

                # 2. Delete all direct chat sessions
                # FIX: Use DirectChatSession
                num_chatrooms, _ = DirectChatSession.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"--- {num_chatrooms} sesiones de chat eliminadas con éxito."
                    )
                )

                # 3. Clear keys and salt from user profiles
                perfiles = PerfilUsuario.objects.all()
                num_profiles_updated = 0
                for perfil in perfiles:
                    perfil.public_key = None
                    perfil.private_key = None
                    perfil.encryption_salt = None
                    perfil.save()
                    num_profiles_updated += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"--- Claves y sales reseteadas en {num_profiles_updated} perfiles de usuario."
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"XXX Ocurrió un error durante la purga: {e}")
            )
            self.stdout.write(
                self.style.WARNING("--- La operación se ha revertido debido al error.")
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                ">>> ¡PURGA COMPLETADA! La base de datos está limpia de datos de prueba."
            )
        )
