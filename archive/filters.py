import django_filters

from .models import Archive


class ArchiveFilter(django_filters.FilterSet):
    survey_type = django_filters.CharFilter(lookup_expr="icontains")
    level = django_filters.CharFilter(lookup_expr="icontains")
    start_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Archive
        fields = ["survey_type", "level", "start_date", "end_date"]
