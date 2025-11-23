from django.apps import AppConfig


class AssessmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "assessment"
    verbose_name = "Evaluaciones"

    def ready(self):
        import assessment.signals
