from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .models import SOP
from .serializers import AdminSOPSerializer, SOPSerializer


class SOPListCreateAPIView(ListCreateAPIView):
    queryset = SOP.objects.filter(is_admin_only=False).order_by("-created_at")
    serializer_class = SOPSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class AdminSOPListAPIView(ListCreateAPIView):
    serializer_class = AdminSOPSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get_queryset(self):
        filter_param = self.request.query_params.get("filter")
        if filter_param == "all":
            return SOP.objects.all().order_by("-created_at")
        elif filter_param == "public":
            return SOP.objects.filter(is_admin_only=False).order_by("-created_at")
        return SOP.objects.filter(is_admin_only=True).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(is_admin_only=True)


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
        if (
            user
            and user.is_authenticated
            and (user.role == "superadmin" or user.is_staff or user.is_superuser)
        ):
            return SOP.objects.all()
        return SOP.objects.filter(is_admin_only=False)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
