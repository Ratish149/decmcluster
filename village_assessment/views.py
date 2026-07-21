from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import VillageAssessmentFilter
from .models import VillageAssessment, VillageAssessmentImport
from .serializers import VillageAssessmentImportSerializer, VillageAssessmentSerializer


class VillageAssessmentListCreateAPIView(ListCreateAPIView):
    queryset = VillageAssessment.objects.all().order_by(
        "-assessment_date", "-created_at"
    )
    serializer_class = VillageAssessmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_class = VillageAssessmentFilter
    search_fields = [
        "province",
        "area_council",
        "village_name",
        "village_other",
        "validation_status",
    ]
    ordering_fields = ["assessment_date", "idp_individuals_total", "created_at"]


class VillageAssessmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = VillageAssessment.objects.all()
    serializer_class = VillageAssessmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class VillageAssessmentImportListCreateAPIView(ListCreateAPIView):
    queryset = (
        VillageAssessmentImport.objects
        .all()
        .select_related("uploaded_by", "verified_by")
        .order_by("-created_at")
    )
    serializer_class = VillageAssessmentImportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(uploaded_by=self.request.user)
        else:
            serializer.save()


class VillageAssessmentImportRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = VillageAssessmentImport.objects.all().select_related(
        "uploaded_by", "verified_by"
    )
    serializer_class = VillageAssessmentImportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
