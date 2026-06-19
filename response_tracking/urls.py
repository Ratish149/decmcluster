from django.urls import path

from .views import ResponseTrackingDetailAPIView, ResponseTrackingListCreateAPIView

urlpatterns = [
    path(
        "response-tracking/",
        ResponseTrackingListCreateAPIView.as_view(),
        name="response-tracking-list-create",
    ),
    path(
        "response-tracking/<int:pk>/",
        ResponseTrackingDetailAPIView.as_view(),
        name="response-tracking-detail",
    ),
]
