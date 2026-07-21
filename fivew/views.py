from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import FiveWActivityFilter
from .models import FiveWActivity, FiveWImport
from .serializers import FiveWActivitySerializer, FiveWImportSerializer


class FiveWActivityListCreateAPIView(ListCreateAPIView):
    queryset = FiveWActivity.objects.all().order_by("-created_at")
    serializer_class = FiveWActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_class = FiveWActivityFilter
    search_fields = [
        "donor",
        "reporting_org_name",
        "activity",
        "indicator",
        "state_abyei",
        "cluster_name",
    ]
    ordering_fields = ["created_at", "total_beneficiaries_reached", "target"]


class FiveWActivityRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = FiveWActivity.objects.all()
    serializer_class = FiveWActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FiveWImportListCreateAPIView(ListCreateAPIView):
    queryset = (
        FiveWImport.objects.all()
        .select_related("uploaded_by", "verified_by")
        .order_by("-created_at")
    )
    serializer_class = FiveWImportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the uploaded_by field to the current user if authenticated
        if self.request.user.is_authenticated:
            serializer.save(uploaded_by=self.request.user)
        else:
            serializer.save()


class FiveWImportRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = FiveWImport.objects.all().select_related("uploaded_by", "verified_by")
    serializer_class = FiveWImportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
