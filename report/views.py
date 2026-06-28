from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .models import Report
from .serializers import AdminReportSerializer, ReportSerializer


class ReportListCreateAPIView(ListCreateAPIView):
    serializer_class = ReportSerializer
    pagination_class = CustomPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]

    def get_queryset(self):
        queryset = Report.objects.filter(is_situation_report=False).order_by(
            "-created_at"
        )
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class ReportDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class AdminReportListAPIView(ListCreateAPIView):
    serializer_class = AdminReportSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get_queryset(self):
        filter_param = self.request.query_params.get("filter")
        if filter_param == "all":
            return Report.objects.all().order_by("-created_at")
        elif filter_param == "public":
            return Report.objects.filter(is_situation_report=False).order_by(
                "-created_at"
            )
        return Report.objects.filter(is_situation_report=True).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(is_situation_report=True)
