# /academic_chat/apps.py
from django.apps import AppConfig


class AcademicChatConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "academic_chat"
    verbose_name = "Chats Académicos"

    def ready(self):
        """
        Sobrescribimos el método ready para importar y registrar
        las señales de la aplicación cuando Django se inicia.
        """
        try:
            import academic_chat.signals
        except ImportError:
            pass
