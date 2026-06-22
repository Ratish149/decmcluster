from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .models import MeetingMinute
from .serializers import MeetingMinuteSerializer


class MeetingMinuteListCreateAPIView(ListCreateAPIView):
    queryset = MeetingMinute.objects.all().order_by("-created_at")
    serializer_class = MeetingMinuteSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    permission_classes = [IsAuthenticated, RoleBasedPermission]


class MeetingMinuteDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = MeetingMinute.objects.all()
    serializer_class = MeetingMinuteSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]
