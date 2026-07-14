from django.apps import AppConfig


class DisplacementConfig(AppConfig):
    name = 'displacement'

    def ready(self):
        import displacement.signals  # noqa: F401

