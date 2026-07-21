from django.urls import path

from .views import (
    VillageAssessmentImportListCreateAPIView,
    VillageAssessmentImportRetrieveUpdateDestroyAPIView,
    VillageAssessmentListCreateAPIView,
    VillageAssessmentRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "village-assessments/",
        VillageAssessmentListCreateAPIView.as_view(),
        name="village-assessment-list-create",
    ),
    path(
        "village-assessments/<int:pk>/",
        VillageAssessmentRetrieveUpdateDestroyAPIView.as_view(),
        name="village-assessment-detail",
    ),
    path(
        "village-assessment-imports/",
        VillageAssessmentImportListCreateAPIView.as_view(),
        name="village-assessment-import-list-create",
    ),
    path(
        "village-assessment-imports/<int:pk>/",
        VillageAssessmentImportRetrieveUpdateDestroyAPIView.as_view(),
        name="village-assessment-import-detail",
    ),
]
