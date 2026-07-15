from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import RoleBasedPermission

from .models import (
    Banner,
    DashboardSummary,
    EvacuationCentreList,
    EvacuationCentreLocationSummary,
    HistoricalEvents,
    PowerBiIframe,
    ProvinceSectorSummary,
    ResponseTrackingSummary,
)
from .serializers import (
    BannerSerializer,
    DashboardSummarySerializer,
    EvacuationCentreListSerializer,
    EvacuationCentreLocationSummarySerializer,
    HistoricalEventsSerializer,
    PowerBiIframeSerializer,
    ProvinceSectorSummarySerializer,
    ResponseTrackingSummarySerializer,
)


class DashboardSummaryListCreateAPIView(ListCreateAPIView):
    serializer_class = DashboardSummarySerializer

    def get_queryset(self):
        # Automatically ensure the singleton instance exists and return it
        DashboardSummary.load()
        return DashboardSummary.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]

    def perform_create(self, serializer):
        # If the singleton already exists, update it instead of creating a new one
        instance = DashboardSummary.objects.filter(pk=1).first()
        if instance:
            serializer.instance = instance
        serializer.save()


class DashboardSummaryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = DashboardSummary.objects.all()
    serializer_class = DashboardSummarySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class EvacuationCentreLocationSummaryListCreateAPIView(ListCreateAPIView):
    queryset = EvacuationCentreLocationSummary.objects.all().order_by("order")
    serializer_class = EvacuationCentreLocationSummarySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class EvacuationCentreLocationSummaryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EvacuationCentreLocationSummary.objects.all()
    serializer_class = EvacuationCentreLocationSummarySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class ProvinceSectorSummaryListCreateAPIView(ListCreateAPIView):
    # Retrieve data ordered by highest percentage first
    queryset = ProvinceSectorSummary.objects.all().order_by("-percentage")
    serializer_class = ProvinceSectorSummarySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class ProvinceSectorSummaryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProvinceSectorSummary.objects.all()
    serializer_class = ProvinceSectorSummarySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class HistoricalEventsListCreateAPIView(ListCreateAPIView):
    # Retrieve data ordered chronologically by year
    queryset = HistoricalEvents.objects.all().order_by("year")
    serializer_class = HistoricalEventsSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class HistoricalEventsDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = HistoricalEvents.objects.all()
    serializer_class = HistoricalEventsSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class EvacuationCentreListListCreateAPIView(ListCreateAPIView):
    queryset = EvacuationCentreList.objects.all().order_by("id")
    serializer_class = EvacuationCentreListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["site_name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class EvacuationCentreListDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EvacuationCentreList.objects.all()
    serializer_class = EvacuationCentreListSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class ResponseTrackingSummaryListCreateAPIView(ListCreateAPIView):
    queryset = ResponseTrackingSummary.objects.all().order_by("id")
    serializer_class = ResponseTrackingSummarySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class ResponseTrackingSummaryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ResponseTrackingSummary.objects.all()
    serializer_class = ResponseTrackingSummarySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class BannerListCreateAPIView(ListCreateAPIView):
    queryset = Banner.objects.all().order_by("-id")
    serializer_class = BannerSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class BannerDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class PowerBiIframeListCreateAPIView(ListCreateAPIView):
    queryset = PowerBiIframe.objects.all().order_by("-id")
    serializer_class = PowerBiIframeSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class PowerBiIframeDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = PowerBiIframe.objects.all()
    serializer_class = PowerBiIframeSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]
