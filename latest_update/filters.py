import django_filters

from .models import Category, LatestUpdate


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    slug = django_filters.CharFilter(field_name="slug", lookup_expr="exact")

    class Meta:
        model = Category
        fields = ["name", "slug"]


class LatestUpdateFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="category__slug", lookup_expr="exact"
    )
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    is_featured = django_filters.BooleanFilter(field_name="is_featured")
    slug = django_filters.CharFilter(field_name="slug", lookup_expr="exact")
    start_date = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    end_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = LatestUpdate
        fields = [
            "category",
            "title",
            "is_featured",
            "slug",
            "start_date",
            "end_date",
        ]
