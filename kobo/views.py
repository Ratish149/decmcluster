from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import RoleBasedPermission

from .filters import KoboSubmissionFilter
from .models import KoboAsset, KoboSubmission
from .serializers import KoboAssetSerializer, KoboSubmissionSerializer
from .services import KoboService


class KoboAssetListCreateAPIView(ListCreateAPIView):
    """
    API view to list or register new Kobo assets/projects manually.
    """

    queryset = KoboAsset.objects.all().order_by("-created_at")
    serializer_class = KoboAssetSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]


class KoboAssetDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a registered Kobo asset/project using its unique asset_uid.
    """

    queryset = KoboAsset.objects.all()
    serializer_class = KoboAssetSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    lookup_field = "asset_uid"


class KoboAssetDiscoveryAPIView(APIView):
    """
    Fetch all forms from the KoboToolbox account and register/update them in the local database.
    """

    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def post(self, request, *args, **kwargs):
        service = KoboService()
        try:
            synced_assets = service.sync_registered_assets()
            serializer = KoboAssetSerializer(synced_assets, many=True)
            return Response(
                {
                    "message": f"Successfully retrieved and synced {len(synced_assets)} survey forms from KoboToolbox.",
                    "assets": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class KoboAssetSyncAPIView(APIView):
    """
    Synchronizes submissions data of a specific Kobo form into the local database.
    """

    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def post(self, request, asset_uid, *args, **kwargs):
        service = KoboService()
        try:
            sync_count = service.sync_submissions(asset_uid)
            return Response(
                {
                    "message": "Project data synchronization completed successfully.",
                    "synced_submissions_count": sync_count,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as ve:
            return Response(
                {"error": str(ve)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class KoboSubmissionListAPIView(ListAPIView):
    """
    List and filter synchronized Kobo submissions from the local database.
    """

    queryset = (
        KoboSubmission.objects.all().select_related("asset").order_by("-submitted_at")
    )
    serializer_class = KoboSubmissionSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    filterset_class = KoboSubmissionFilter


class KoboAssetRawDataAPIView(APIView):
    """
    Directly fetches raw submissions data from KoboToolbox for a specific asset UID.
    No authentication required to call this endpoint.
    """

    permission_classes = [AllowAny]

    def get(self, request, asset_uid, *args, **kwargs):
        service = KoboService()
        try:
            data = service.fetch_raw_submissions(asset_uid)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class KoboRestServiceWebhookAPIView(APIView):
    """
    Receives POST payloads from KoboToolbox REST Service.
    Configure this URL as the REST Service endpoint in your KoboToolbox project dashboard.
    No authentication required (KoboToolbox calls this endpoint).
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.data
        print("=" * 60)
        print("KoboToolbox Webhook Received:")
        print(payload)
        print("=" * 60)
        return Response(
            {
                "status": "received",
                "payload": payload,
            },
            status=status.HTTP_200_OK,
        )
