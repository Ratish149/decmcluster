from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import EmergencyAlertFilter
from .models import EmergencyAlert
from .selectors.emergency_alert_selector import get_emergency_alerts
from .serializers import EmergencyAlertSerializer


class EmergencyAlertListCreateAPIView(ListCreateAPIView):
    queryset = get_emergency_alerts()
    serializer_class = EmergencyAlertSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = EmergencyAlertFilter
    search_fields = ["title"]
    ordering_fields = ["created_at", "updated_at", "title"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class EmergencyAlertDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EmergencyAlert.objects.all()
    serializer_class = EmergencyAlertSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
