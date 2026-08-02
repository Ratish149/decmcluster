from django.urls import path

from .views import (
    AnnouncementDetailAPIView,
    AnnouncementListCreateAPIView,
)

urlpatterns = [
    path(
        "announcements/",
        AnnouncementListCreateAPIView.as_view(),
        name="announcement-list-create",
    ),
    path(
        "announcements/<slug:slug>/",
        AnnouncementDetailAPIView.as_view(),
        name="announcement-detail",
    ),
]
