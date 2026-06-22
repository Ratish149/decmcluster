from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission

from .models import UsefulLink
from .serializers import UsefulLinkSerializer


class UsefulLinkListCreateAPIView(ListCreateAPIView):
    queryset = UsefulLink.objects.all().order_by("-created_at")
    serializer_class = UsefulLinkSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class UsefulLinkDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UsefulLink.objects.all()
    serializer_class = UsefulLinkSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
