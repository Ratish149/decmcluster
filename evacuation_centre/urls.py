from django.urls import path

from .views import (
    EvacuationCentreDetailAPIView,
    EvacuationCentreExportAPIView,
    EvacuationCentreImportAPIView,
    EvacuationCentreListCreateAPIView,
    EvacuationCentreMinimalListAPIView,
    EvacuationCentreStatsAPIView,
)

urlpatterns = [
    path(
        "evacuation-centres/",
        EvacuationCentreListCreateAPIView.as_view(),
        name="evacuation-centre-list-create",
    ),
    path(
        "evacuation-centres/location/",
        EvacuationCentreMinimalListAPIView.as_view(),
        name="evacuation-centre-minimal-list",
    ),
    path(
        "evacuation-centres/import/",
        EvacuationCentreImportAPIView.as_view(),
        name="evacuation-centre-import",
    ),
    path(
        "evacuation-centres/export/",
        EvacuationCentreExportAPIView.as_view(),
        name="evacuation-centre-export",
    ),
    path(
        "evacuation-centres/stats/",
        EvacuationCentreStatsAPIView.as_view(),
        name="evacuation-centre-stats",
    ),
    path(
        "evacuation-centres/<int:pk>/",
        EvacuationCentreDetailAPIView.as_view(),
        name="evacuation-centre-detail",
    ),
]
