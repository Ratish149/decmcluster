from django.contrib import admin
from unfold.admin import ModelAdmin

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


@admin.register(DashboardSummary)
class DashboardSummaryAdmin(ModelAdmin):
    list_display = [
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

    def has_add_permission(self, request):
        # Allow adding only if no instance exists
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Disallow deletion of the singleton instance
        return False


@admin.register(EvacuationCentreLocationSummary)
class EvacuationCentreLocationSummaryAdmin(ModelAdmin):
    list_display = ["id", "province", "ecs", "idps", "order"]
    search_fields = ["province"]


@admin.register(ProvinceSectorSummary)
class ProvinceSectorSummaryAdmin(ModelAdmin):
    list_display = ["id", "title", "percentage"]
    search_fields = ["title"]


@admin.register(HistoricalEvents)
class HistoricalEventsAdmin(ModelAdmin):
    list_display = ["id", "event", "year", "impact"]
    search_fields = ["event", "impact"]
    list_filter = ["year"]


@admin.register(EvacuationCentreList)
class EvacuationCentreListAdmin(ModelAdmin):
    list_display = ["id", "province", "site_name", "type", "status", "hhs"]
    search_fields = ["province", "site_name", "type", "status"]
    list_filter = ["province", "type", "status"]


@admin.register(ResponseTrackingSummary)
class ResponseTrackingSummaryAdmin(ModelAdmin):
    list_display = ["id", "sector", "partner", "status", "coverage"]
    search_fields = ["sector", "partner", "status"]
    list_filter = ["sector", "status"]


@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    list_display = ["id", "title", "image", "created_at", "updated_at"]
    search_fields = ["title", "description"]


@admin.register(PowerBiIframe)
class PowerBiIframeAdmin(ModelAdmin):
    list_display = ["id", "iframe_link", "created_at", "updated_at"]

    def has_add_permission(self, request):
        # Allow adding only if no instance exists
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Disallow deletion of the singleton instance
        return False
