from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import DisplacementFilter
from .models import Displacement
from .selectors import get_displacement_stats
from .serializers import DisplacementSerializer, FileImportSerializer
from .services.import_service import (
    import_displacements_from_csv,
    import_displacements_from_excel,
)


class DisplacementListCreateAPIView(ListCreateAPIView):
    queryset = Displacement.objects.all().order_by("-reporting_date")
    serializer_class = DisplacementSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DisplacementFilter
    search_fields = ["operation", "admin1_name", "admin2_name", "displacement_reason"]
    permission_classes = [IsAuthenticated, RoleBasedPermission]


class DisplacementDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Displacement.objects.all()
    serializer_class = DisplacementSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]


class DisplacementImportAPIView(GenericAPIView):
    parser_classes = [MultiPartParser]
    # permission_classes = [IsAuthenticated, RoleBasedPermission]
    serializer_class = FileImportSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = serializer.validated_data["file"]
        file_name = uploaded_file.name.lower()

        try:
            if file_name.endswith(".csv"):
                created_count, updated_count = import_displacements_from_csv(
                    uploaded_file
                )
            else:
                created_count, updated_count = import_displacements_from_excel(
                    uploaded_file
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


class DisplacementStatsAPIView(APIView):
    # permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get(self, request, *args, **kwargs):
        queryset = Displacement.objects.all()
        filterset = DisplacementFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        stats_data = get_displacement_stats(queryset)
        return Response(stats_data, status=status.HTTP_200_OK)
