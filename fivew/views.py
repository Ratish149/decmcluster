from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from decmcluster.pagination import CustomPagination

from .filters import FiveWActivityFilter
from .models import FiveWActivity, FiveWImport
from .serializers import FiveWActivitySerializer, FiveWImportSerializer
from .services.export_service import generate_fivew_csv


class FiveWActivityListCreateAPIView(ListCreateAPIView):
    queryset = FiveWActivity.objects.all().order_by("-created_at")
    serializer_class = FiveWActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    pagination_class = CustomPagination

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
    pagination_class = CustomPagination

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


class FiveWActivityExportAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        queryset = FiveWActivity.objects.all().order_by("created_at")
        filterset = FiveWActivityFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs

        columns_param = request.GET.get("columns", "")
        requested_columns = None
        if columns_param:
            requested_columns = [
                col.strip() for col in columns_param.split(",") if col.strip()
            ]

        return generate_fivew_csv(queryset, requested_columns)
