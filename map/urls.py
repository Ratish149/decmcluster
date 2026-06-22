from django.urls import path

from .views import (
    MapCategoryDetailAPIView,
    MapCategoryListCreateAPIView,
    MapDetailAPIView,
    MapListCreateAPIView,
)

urlpatterns = [
    path(
        "map-category/",
        MapCategoryListCreateAPIView.as_view(),
        name="map-category-list-create",
    ),
    path(
        "map-category/<str:slug>/",
        MapCategoryDetailAPIView.as_view(),
        name="map-category-detail",
    ),
    path(
        "map/",
        MapListCreateAPIView.as_view(),
        name="map-list-create",
    ),
    path(
        "map/<int:pk>/",
        MapDetailAPIView.as_view(),
        name="map-detail",
    ),
]
