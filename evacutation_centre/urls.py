from django.urls import path

from .views import (
    EvacutationCentreDetailAPIView,
    EvacutationCentreImportAPIView,
    EvacutationCentreListCreateAPIView,
    EvacutationCentreMinimalListAPIView,
    EvacutationCentreStatsAPIView,
)

urlpatterns = [
    path(
        "evacuation-centres/",
        EvacutationCentreListCreateAPIView.as_view(),
        name="evacuation-centre-list-create",
    ),
    path(
        "evacuation-centres/location/",
        EvacutationCentreMinimalListAPIView.as_view(),
        name="evacuation-centre-minimal-list",
    ),
    path(
        "evacuation-centres/import/",
        EvacutationCentreImportAPIView.as_view(),
        name="evacuation-centre-import",
    ),
    path(
        "evacuation-centres/stats/",
        EvacutationCentreStatsAPIView.as_view(),
        name="evacuation-centre-stats",
    ),
    path(
        "evacuation-centres/<int:pk>/",
        EvacutationCentreDetailAPIView.as_view(),
        name="evacuation-centre-detail",
    ),
]
