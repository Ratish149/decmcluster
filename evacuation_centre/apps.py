from django.apps import AppConfig


class EvacuationCentreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'evacuation_centre'

    def ready(self):
        import evacuation_centre.signals

