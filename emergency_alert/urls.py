from django.urls import path

from .views import (
    EmergencyAlertDetailAPIView,
    EmergencyAlertListCreateAPIView,
)

urlpatterns = [
    path(
        "emergency-alerts/",
        EmergencyAlertListCreateAPIView.as_view(),
        name="emergency-alert-list-create",
    ),
    path(
        "emergency-alerts/<slug:slug>/",
        EmergencyAlertDetailAPIView.as_view(),
        name="emergency-alert-detail",
    ),
]
