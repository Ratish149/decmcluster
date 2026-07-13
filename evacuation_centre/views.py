from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import EvacutationCentreFilter
from .models import EvacutationCentre
from .selectors import get_evacuation_centre_stats
from .serializers import (
    EvacutationCentreMinimalSerializer,
    EvacutationCentreSerializer,
    FileImportSerializer,
)
from .services.import_service import (
    import_evacuation_centres_from_csv,
    import_evacuation_centres_from_excel,
)


class EvacutationCentreListCreateAPIView(ListCreateAPIView):
    queryset = EvacutationCentre.objects.all().order_by("-created_at")
    serializer_class = EvacutationCentreSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EvacutationCentreFilter
    search_fields = ["compound_name", "province", "area_council", "island", "village"]
    permission_classes = [IsAuthenticated, RoleBasedPermission]


class EvacutationCentreDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EvacutationCentre.objects.all()
    serializer_class = EvacutationCentreSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]


class EvacutationCentreImportAPIView(GenericAPIView):
    parser_classes = [MultiPartParser]
    # permission_classes = [IsAuthenticated, RoleBasedPermission]
    serializer_class = FileImportSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        excel_file = serializer.validated_data["file"]
        file_name = excel_file.name.lower()

        try:
            if file_name.endswith(".csv"):
                created_count, updated_count = import_evacuation_centres_from_csv(
                    excel_file
                )
            else:
                created_count, updated_count = import_evacuation_centres_from_excel(
                    excel_file
                )
            return Response(
                {
                    "message": "Import completed successfully.",
                    "created": created_count,
                    "updated": updated_count,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred while processing the file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EvacutationCentreStatsAPIView(APIView):
    # permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get(self, request, *args, **kwargs):
        queryset = EvacutationCentre.objects.all()
        filterset = EvacutationCentreFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        stats_data = get_evacuation_centre_stats(queryset)
        return Response(stats_data, status=status.HTTP_200_OK)


class EvacutationCentreMinimalListAPIView(ListAPIView):
    queryset = (
        EvacutationCentre.objects
        .all()
        .order_by("-created_at")
        .only(
            "id",
            "compound_name",
            "latitude",
            "longitude",
            "is_ec_owner_approved",
            "is_ec_govt_approved",
            "province",
        )
    )
    serializer_class = EvacutationCentreMinimalSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EvacutationCentreFilter
    search_fields = ["compound_name", "province", "area_council", "island", "village"]
