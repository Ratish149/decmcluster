from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

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
    serializer_class = MapSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]

    def get_queryset(self):
        queryset = Map.objects.all().order_by("-created_at")
        category_slug = self.request.query_params.get("category")
        if category_slug:
            queryset = queryset.filter(category_slug=category_slug)
        return queryset


class MapDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
