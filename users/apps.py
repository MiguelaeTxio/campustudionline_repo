# /users/apps.py
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'

from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    # --- INICIO DE LA MODIFICACIÓN ---
    # Cambiamos el nombre que se muestra en el panel de administración
    # para que sea más específico y claro.
    verbose_name = "Gestión de Usuarios y Perfiles"
    # --- FIN DE LA MODIFICACIÓN ---

    def ready(self):
        """
        Se ejecuta cuando la aplicación está lista.
        Importamos las señales aquí para que se conecten correctamente.
        """
        try:
            # Esta línea es la que hace la magia: importa y conecta las señales.
            import users.signals

            logger.info("Señales de la app 'users' conectadas correctamente.")
        except ImportError:
            logger.warning(
                "No se pudo importar users.signals (puede que el archivo no exista aún)."
            )
        except Exception as e:
            logger.error(
                f"Error al intentar conectar señales de 'users': {e}", exc_info=True
            )
