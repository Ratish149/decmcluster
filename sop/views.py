from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import SOPFilter
from .models import SOP
from .serializers import AdminSOPSerializer, SOPSerializer
from .utils import send_sop_verification_email


class SOPListCreateAPIView(ListCreateAPIView):
    pagination_class = CustomPagination
    serializer_class = SOPSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = SOPFilter
    search_fields = ["name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]

    def get_queryset(self):
        return (
            SOP.objects
            .select_related("uploaded_by", "verified_by")
            .prefetch_related("comments", "comments__author")
            .filter(is_admin_only=False)
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class AdminSOPListAPIView(ListCreateAPIView):
    serializer_class = AdminSOPSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = SOPFilter
    search_fields = ["name"]

    def get_queryset(self):
        filter_param = self.request.query_params.get("filter")
        base_qs = SOP.objects.select_related(
            "uploaded_by", "verified_by"
        ).prefetch_related("comments", "comments__author")
        if filter_param == "all":
            return base_qs.all().order_by("-created_at")
        elif filter_param == "public":
            return base_qs.filter(is_admin_only=False).order_by("-created_at")
        return base_qs.filter(is_admin_only=True).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(is_admin_only=True, uploaded_by=self.request.user)


class SOPDetailAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"

    def get_serializer_class(self):
        user = self.request.user
        if (
            user
            and user.is_authenticated
            and (user.role == "superadmin" or user.is_staff or user.is_superuser)
        ):
            return AdminSOPSerializer
        return SOPSerializer

    def get_queryset(self):
        user = self.request.user
        base_qs = SOP.objects.select_related(
            "uploaded_by", "verified_by"
        ).prefetch_related("comments", "comments__author")
        if (
            user
            and user.is_authenticated
            and (user.role == "superadmin" or user.is_staff or user.is_superuser)
        ):
            return base_qs.all()
        return base_qs.filter(is_admin_only=False)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]

    def perform_update(self, serializer):
        status_value = self.request.data.get("status")
        if status_value == SOP.StatusChoices.VERIFIED:
            serializer.save(verified_by=self.request.user)
        else:
            serializer.save()


class SOPReverifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            instance = SOP.objects.get(pk=pk)
        except SOP.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if instance.uploaded_by != request.user:
            return Response(
                {"detail": "Only the uploader can resubmit for verification."},
                status=status.HTTP_403_FORBIDDEN,
            )

        instance.status = SOP.StatusChoices.UNVERIFIED
        instance.verified_by = None
        instance.save()

        comment_value = request.data.get("comment")
        if comment_value:
            from .models import SOPComment

            SOPComment.objects.create(
                sop=instance,
                author=request.user,
                comment=comment_value,
            )

        # Resend email to admin
        send_sop_verification_email(instance, comment=comment_value)

        serializer = SOPSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
