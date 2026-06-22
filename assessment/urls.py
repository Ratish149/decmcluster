from django.urls import path

from .views import (
    AssessmentDetailAPIView,
    AssessmentListCreateAPIView,
    AssessmentRegistryDetailAPIView,
    AssessmentRegistryListCreateAPIView,
    AssessmentResultDetailAPIView,
    AssessmentResultListCreateAPIView,
    AssessmentStatsDetailAPIView,
    AssessmentStatsListCreateAPIView,
)

urlpatterns = [
    path(
        "assessment/",
        AssessmentListCreateAPIView.as_view(),
        name="assessment-list-create",
    ),
    path(
        "assessment/<slug:slug>/",
        AssessmentDetailAPIView.as_view(),
        name="assessment-detail",
    ),
    path(
        "assessment/<slug:slug>/result/",
        AssessmentResultListCreateAPIView.as_view(),
        name="assessment-result-list-create",
    ),
    path(
        "assessment/<slug:slug>/result/<int:pk>/",
        AssessmentResultDetailAPIView.as_view(),
        name="assessment-result-detail",
    ),
    path(
        "assessment-registry/",
        AssessmentRegistryListCreateAPIView.as_view(),
        name="assessment-registry-list-create",
    ),
    path(
        "assessment-registry/<int:pk>/",
        AssessmentRegistryDetailAPIView.as_view(),
        name="assessment-registry-detail",
    ),
    path(
        "assessment-stats/",
        AssessmentStatsListCreateAPIView.as_view(),
        name="assessment-stats-list-create",
    ),
    path(
        "assessment-stats/<int:pk>/",
        AssessmentStatsDetailAPIView.as_view(),
        name="assessment-stats-detail",
    ),
]
