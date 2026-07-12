from django.urls import path

from .views import (
    DisplacementDetailAPIView,
    DisplacementImportAPIView,
    DisplacementListCreateAPIView,
    DisplacementStatsAPIView,
)

urlpatterns = [
    path(
        "displacements/",
        DisplacementListCreateAPIView.as_view(),
        name="displacement-list-create",
    ),
    path(
        "displacements/stats/",
        DisplacementStatsAPIView.as_view(),
        name="displacement-stats",
    ),
    path(
        "displacements/import/",
        DisplacementImportAPIView.as_view(),
        name="displacement-import",
    ),
    path(
        "displacements/<int:pk>/",
        DisplacementDetailAPIView.as_view(),
        name="displacement-detail",
    ),
]
