from django.urls import path

from .views import ReportDetailAPIView, ReportListCreateAPIView

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
]
