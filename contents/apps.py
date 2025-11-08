# /home/MiguelAeTxio/CampuStudiOnline/contents/apps.py
from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class ContentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "contents"
    verbose_name = "Gestión de Contenidos"

    def ready(self):
        """
        Se ejecuta cuando la aplicación está lista.
        Importamos las señales aquí para que se conecten correctamente.
        """
        try:
            import contents.signals
            logger.info("Signals for 'contents' app connected successfully.")
        except ImportError:
            logger.warning(
                "Could not import contents.signals (the file may not exist yet)."
            )
        except Exception as e:
            logger.error(
                f"Error connecting signals for 'contents': {e}", exc_info=True
            )
