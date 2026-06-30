import django_filters

from .models import Report


class ReportFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = Report
        fields = ["status"]
