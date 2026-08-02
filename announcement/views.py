from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import AnnouncementFilter
from .models import Announcement
from .selectors.announcement_selector import get_announcements
from .serializers import AnnouncementSerializer


class AnnouncementListCreateAPIView(ListCreateAPIView):
    queryset = get_announcements()
    serializer_class = AnnouncementSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = AnnouncementFilter
    search_fields = ["title"]
    ordering_fields = ["created_at", "updated_at", "title"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class AnnouncementDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
