from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .models import SOP
from .serializers import SOPSerializer


class SOPListCreateAPIView(ListCreateAPIView):
    queryset = SOP.objects.all().order_by("-created_at")
    serializer_class = SOPSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class SOPDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SOP.objects.all()
    serializer_class = SOPSerializer
    lookup_field = "pk"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
