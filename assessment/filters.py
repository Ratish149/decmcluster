import django_filters

from .models import Assessment


class AssessmentFilter(django_filters.FilterSet):
    is_public = django_filters.BooleanFilter(field_name="is_public")

    class Meta:
        model = Assessment
        fields = ["is_public"]
