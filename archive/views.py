from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import ArchiveFilter
from .models import Archive
from .selectors.archive_selector import get_archives
from .serializers import ArchiveSerializer


class ArchiveListCreateAPIView(ListCreateAPIView):
    queryset = get_archives()
    serializer_class = ArchiveSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ArchiveFilter
    search_fields = ["survey_type", "level"]
    ordering_fields = ["date", "created_at", "updated_at", "survey_type", "level"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class ArchiveDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
