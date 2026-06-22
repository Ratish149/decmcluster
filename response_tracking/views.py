from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission

from .models import ResponseTracking
from .serializers import ResponseTrackingSerializer


class ResponseTrackingListCreateAPIView(ListCreateAPIView):
    serializer_class = ResponseTrackingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]

    def get_queryset(self):
        queryset = ResponseTracking.objects.all().order_by("-created_at")
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class ResponseTrackingDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ResponseTracking.objects.all()
    serializer_class = ResponseTrackingSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
