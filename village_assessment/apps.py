from django.apps import AppConfig


class VillageAssessmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "village_assessment"

    def ready(self):
        import village_assessment.signals  # noqa: F401
