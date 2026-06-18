from django.urls import path

from .views import (
    AssessmentDetailAPIView,
    AssessmentListCreateAPIView,
    AssessmentResultDetailAPIView,
    AssessmentResultListCreateAPIView,
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
]
