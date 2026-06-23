import django_filters

from .models import ContactList


class ContactListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    organization = django_filters.CharFilter(lookup_expr="icontains")
    type = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = ContactList
        fields = ["name", "organization", "type"]
