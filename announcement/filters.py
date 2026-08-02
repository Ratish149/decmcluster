import django_filters

from .models import Announcement


class AnnouncementFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    start_date = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    end_date = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    class Meta:
        model = Announcement
        fields = ["title", "start_date", "end_date"]
