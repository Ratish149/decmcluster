from django.urls import path

from .views import (
    DisplacementDetailAPIView,
    DisplacementExportAPIView,
    DisplacementImportAPIView,
    DisplacementListCreateAPIView,
    DisplacementStatsAPIView,
    DisplacementUniqueFiltersAPIView,
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
        "displacements/export/",
        DisplacementExportAPIView.as_view(),
        name="displacement-export",
    ),
    path(
        "displacements/unique-filters/",
        DisplacementUniqueFiltersAPIView.as_view(),
        name="displacement-unique-filters",
    ),
    path(
        "displacements/<int:pk>/",
        DisplacementDetailAPIView.as_view(),
        name="displacement-detail",
    ),
]
