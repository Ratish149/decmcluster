import django_filters

from .models import LatestUpdate


class LatestUpdateFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    is_featured = django_filters.BooleanFilter(field_name="is_featured")
    slug = django_filters.CharFilter(field_name="slug", lookup_expr="exact")
    created_at_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_at_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    class Meta:
        model = LatestUpdate
        fields = [
            "title",
            "is_featured",
            "slug",
            "created_at_after",
            "created_at_before",
        ]
