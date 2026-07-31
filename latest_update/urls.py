from django.urls import path

from .views import (
    CategoryDetailAPIView,
    CategoryListCreateAPIView,
    LatestUpdateDetailAPIView,
    LatestUpdateListCreateAPIView,
)

urlpatterns = [
    path(
        "latest-update-categories/",
        CategoryListCreateAPIView.as_view(),
        name="category-list-create",
    ),
    path(
        "latest-update-categories/<int:pk>/",
        CategoryDetailAPIView.as_view(),
        name="category-detail",
    ),
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
