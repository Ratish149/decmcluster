from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import LatestUpdateFilter
from .models import LatestUpdate
from .serializers import LatestUpdateSerializer


class LatestUpdateListCreateAPIView(ListCreateAPIView):
    queryset = LatestUpdate.objects.all().order_by("-created_at")
    serializer_class = LatestUpdateSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = LatestUpdateFilter
    search_fields = [
        "title",
        "short_description",
        "description",
        "thumbnail_alt_desc",
        "meta_title",
        "meta_description",
    ]
    ordering_fields = ["created_at", "updated_at", "title", "is_featured"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class LatestUpdateDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = LatestUpdate.objects.all()
    serializer_class = LatestUpdateSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
