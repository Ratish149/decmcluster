from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import MapFilter
from .models import Map, MapCategory
from .serializers import MapCategorySerializer, MapSerializer


class MapCategoryListCreateAPIView(ListCreateAPIView):
    queryset = MapCategory.objects.all().order_by("-created_at")
    serializer_class = MapCategorySerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class MapCategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = MapCategory.objects.all()
    serializer_class = MapCategorySerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class MapListCreateAPIView(ListCreateAPIView):
    queryset = Map.objects.select_related("category").all().order_by("-created_at")
    serializer_class = MapSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MapFilter
    search_fields = ["name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class MapDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Map.objects.select_related("category").all()
    serializer_class = MapSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
