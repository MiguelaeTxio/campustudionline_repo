from django.apps import AppConfig


class ContentAutomationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "content_automation"
    verbose_name = "Automatización de Contenido"

    def ready(self):
        """
        Importa las señales de la aplicación cuando Django está listo.
        Este es el lugar recomendado por la documentación de Django
        para conectar los receptores de señales.
        """
        import content_automation.signals
