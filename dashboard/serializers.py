from rest_framework import serializers

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


class DashboardSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardSummary
        fields = [
            "id",
            "estimated_idp",
            "evacuation_centres",
            "affected_hhs",
            "villages_assessed",
            "shelter_needs",
            "access_to_basic_services",
            "children_affected",
            "person_with_disabilities",
            "active_partners",
            "response_coverage",
        ]
        read_only_fields = ["id"]


class EvacuationCentreLocationSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = EvacuationCentreLocationSummary
        fields = [
            "id",
            "province",
            "ecs",
            "idps",
            "order",
        ]
        read_only_fields = ["id"]


class ProvinceSectorSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvinceSectorSummary
        fields = [
            "id",
            "title",
            "percentage",
        ]
        read_only_fields = ["id"]


class HistoricalEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalEvents
        fields = [
            "id",
            "event",
            "year",
            "impact",
        ]
        read_only_fields = ["id"]


class EvacuationCentreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvacuationCentreList
        fields = [
            "id",
            "province",
            "site_name",
            "type",
            "status",
            "hhs",
        ]
        read_only_fields = ["id"]


class ResponseTrackingSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseTrackingSummary
        fields = [
            "id",
            "sector",
            "partner",
            "status",
            "coverage",
        ]
        read_only_fields = ["id"]


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = [
            "id",
            "title",
            "description",
            "image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PowerBiIframeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerBiIframe
        fields = [
            "id",
            "name",
            "iframe_link",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
