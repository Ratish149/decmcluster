from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import AssessmentFilter
from .models import Assessment, AssessmentRegistry, AssessmentResult, AssessmentStats
from .serializers import (
    AssessmentRegistrySerializer,
    AssessmentResultSerializer,
    AssessmentSerializer,
    AssessmentStatsSerializer,
)


class AssessmentListCreateAPIView(ListCreateAPIView):
    queryset = Assessment.objects.all().order_by("-created_at")
    serializer_class = AssessmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = AssessmentFilter
    search_fields = ["name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class AssessmentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class AssessmentResultListCreateAPIView(ListCreateAPIView):
    serializer_class = AssessmentResultSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return (
            AssessmentResult.objects
            .select_related("assessment")
            .filter(assessment__slug=slug)
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        slug = self.kwargs.get("slug")
        assessment = get_object_or_404(Assessment, slug=slug)
        serializer.save(assessment=assessment)


class AssessmentResultDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AssessmentResultSerializer
    lookup_field = "pk"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return AssessmentResult.objects.select_related("assessment").filter(
            assessment__slug=slug
        )


class AssessmentRegistryListCreateAPIView(ListCreateAPIView):
    queryset = AssessmentRegistry.objects.all().order_by("-created_at")
    serializer_class = AssessmentRegistrySerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class AssessmentRegistryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = AssessmentRegistry.objects.all()
    serializer_class = AssessmentRegistrySerializer
    lookup_field = "pk"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class AssessmentStatsListCreateAPIView(ListCreateAPIView):
    queryset = AssessmentStats.objects.all().order_by("-created_at")
    serializer_class = AssessmentStatsSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class AssessmentStatsDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = AssessmentStats.objects.all()
    serializer_class = AssessmentStatsSerializer
    lookup_field = "pk"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
