from django.urls import path

from .views import (
    AdminReportListAPIView,
    ReportDetailAPIView,
    ReportListCreateAPIView,
    ReportReverifyAPIView,
)

urlpatterns = [
    path(
        "report/",
        ReportListCreateAPIView.as_view(),
        name="report-list-create",
    ),
    path(
        "report/<int:pk>/",
        ReportDetailAPIView.as_view(),
        name="report-detail",
    ),
    path(
        "report/admin/",
        AdminReportListAPIView.as_view(),
        name="report-admin-list",
    ),
    path(
        "report/<int:pk>/reverify/",
        ReportReverifyAPIView.as_view(),
        name="report-reverify",
    ),
]

