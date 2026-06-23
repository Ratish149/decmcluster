from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission

from .filters import ContactListFilter
from .models import ContactList
from .serializers import ContactListSerializer


class ContactListListCreateAPIView(ListCreateAPIView):
    queryset = ContactList.objects.all().order_by("order")
    serializer_class = ContactListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ContactListFilter
    search_fields = ["name", "organization", "cluster", "email"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class ContactListDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ContactList.objects.all()
    serializer_class = ContactListSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
