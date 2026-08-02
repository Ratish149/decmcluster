from django.urls import path

from .views import (
    ArchiveDetailAPIView,
    ArchiveListCreateAPIView,
)

urlpatterns = [
    path(
        "archives/",
        ArchiveListCreateAPIView.as_view(),
        name="archive-list-create",
    ),
    path(
        "archives/<int:pk>/",
        ArchiveDetailAPIView.as_view(),
        name="archive-detail",
    ),
]
