from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import ReportFilter
from .models import Report
from .serializers import AdminReportSerializer, ReportSerializer
from .utils import send_report_verification_email


class ReportListCreateAPIView(ListCreateAPIView):
    serializer_class = ReportSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ReportFilter
    search_fields = ["name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]

    def get_queryset(self):
        queryset = (
            Report.objects.select_related("uploaded_by", "verified_by")
            .prefetch_related("comments", "comments__author")
            .filter(is_situation_report=False)
            .order_by("-created_at")
        )
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class ReportDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = (
        Report.objects.select_related("uploaded_by", "verified_by")
        .prefetch_related("comments", "comments__author")
        .all()
    )
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]

    def perform_update(self, serializer):
        status_value = self.request.data.get("status")
        if status_value == Report.StatusChoices.VERIFIED:
            serializer.save(verified_by=self.request.user)
        else:
            serializer.save()


class AdminReportListAPIView(ListCreateAPIView):
    serializer_class = AdminReportSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ReportFilter
    search_fields = ["name"]

    def get_queryset(self):
        filter_param = self.request.query_params.get("filter")
        base_qs = Report.objects.select_related(
            "uploaded_by", "verified_by"
        ).prefetch_related("comments", "comments__author")
        if filter_param == "all":
            return base_qs.all().order_by("-created_at")
        elif filter_param == "public":
            return base_qs.filter(is_situation_report=False).order_by("-created_at")
        return base_qs.filter(is_situation_report=True).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(is_situation_report=True, uploaded_by=self.request.user)


class ReportReverifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            instance = Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if instance.uploaded_by != request.user:
            return Response(
                {"detail": "Only the uploader can resubmit for verification."},
                status=status.HTTP_403_FORBIDDEN,
            )

        instance.status = Report.StatusChoices.UNVERIFIED
        instance.verified_by = None
        instance.save()

        comment_value = request.data.get("comment")
        if comment_value:
            from .models import ReportComment

            ReportComment.objects.create(
                report=instance,
                author=request.user,
                comment=comment_value,
            )

        # Resend email to admin
        send_report_verification_email(instance, comment=comment_value)

        serializer = ReportSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
