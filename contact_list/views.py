from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import IsSuperAdmin

from .models import ContactList
from .serializers import ContactListSerializer


class ContactListListCreateAPIView(ListCreateAPIView):
    serializer_class = ContactListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "organization", "cluster", "email"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsSuperAdmin()]

    def get_queryset(self):
        queryset = ContactList.objects.all().order_by("order")
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        organization = self.request.query_params.get("organization")
        if organization:
            queryset = queryset.filter(organization__icontains=organization)
        contact_type = self.request.query_params.get("type")
        if contact_type:
            queryset = queryset.filter(type=contact_type)
        return queryset


class ContactListDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ContactList.objects.all()
    serializer_class = ContactListSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsSuperAdmin()]
