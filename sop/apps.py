from django.apps import AppConfig


class SopConfig(AppConfig):
    name = 'sop'

    def ready(self):
        import sop.signals  # noqa: F401
