from django.urls import path

from .views import LatestUpdateDetailAPIView, LatestUpdateListCreateAPIView

urlpatterns = [
    path(
        "latest-updates/",
        LatestUpdateListCreateAPIView.as_view(),
        name="latest-update-list-create",
    ),
    path(
        "latest-updates/<int:pk>/",
        LatestUpdateDetailAPIView.as_view(),
        name="latest-update-detail",
    ),
]
