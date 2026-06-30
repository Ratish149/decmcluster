from django.apps import AppConfig


class MeetingMinuteConfig(AppConfig):
    name = 'meeting_minute'

    def ready(self):
        import meeting_minute.signals  # noqa


