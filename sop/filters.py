import django_filters

from .models import SOP


class SOPFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = SOP
        fields = ["status"]
