from django.apps import AppConfig


class DecmClusterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "decmcluster"

    def ready(self):
        import decmcluster.signals
