from django.apps import AppConfig


class FiveWConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fivew"

    def ready(self):
        import fivew.signals  # noqa: F401
