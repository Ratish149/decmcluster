import django_filters

from .models import MeetingMinute


class MeetingMinuteFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = MeetingMinute
        fields = ["status"]
