import django_filters

from .models import EvacutationCentre


class EvacutationCentreFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name="country", lookup_expr="icontains")
    organization = django_filters.CharFilter(
        field_name="organization", lookup_expr="icontains"
    )
    agency = django_filters.CharFilter(field_name="agency", lookup_expr="icontains")
    province = django_filters.CharFilter(field_name="province", lookup_expr="icontains")
    area_council = django_filters.CharFilter(
        field_name="area_council", lookup_expr="icontains"
    )
    island = django_filters.CharFilter(field_name="island", lookup_expr="icontains")
    village = django_filters.CharFilter(field_name="village", lookup_expr="icontains")
    is_ec_owner_approved = django_filters.BooleanFilter(
        field_name="is_ec_owner_approved"
    )
    is_ec_govt_approved = django_filters.BooleanFilter(field_name="is_ec_govt_approved")

    class Meta:
        model = EvacutationCentre
        fields = [
            "country",
            "organization",
            "agency",
            "province",
            "area_council",
            "island",
            "village",
            "is_ec_owner_approved",
            "is_ec_govt_approved",
        ]
