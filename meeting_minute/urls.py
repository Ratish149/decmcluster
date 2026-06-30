from django.urls import path

from .views import (
    MeetingMinuteDetailAPIView,
    MeetingMinuteListCreateAPIView,
    MeetingMinuteReverifyAPIView,
)

urlpatterns = [
    path(
        "meeting-minute/",
        MeetingMinuteListCreateAPIView.as_view(),
        name="meeting-minute-list-create",
    ),
    path(
        "meeting-minute/<int:pk>/",
        MeetingMinuteDetailAPIView.as_view(),
        name="meeting-minute-detail",
    ),
    path(
        "meeting-minute/<int:pk>/reverify/",
        MeetingMinuteReverifyAPIView.as_view(),
        name="meeting-minute-reverify",
    ),
]
