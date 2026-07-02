from django.urls import path

from .views import (
    KoboAssetDetailAPIView,
    KoboAssetDiscoveryAPIView,
    KoboAssetListCreateAPIView,
    KoboAssetRawDataAPIView,
    KoboAssetSyncAPIView,
    KoboRestServiceWebhookAPIView,
    KoboSubmissionListAPIView,
)

urlpatterns = [
    path(
        "kobo/assets/",
        KoboAssetListCreateAPIView.as_view(),
        name="kobo-asset-list-create",
    ),
    path(
        "kobo/assets/discover/",
        KoboAssetDiscoveryAPIView.as_view(),
        name="kobo-asset-discover",
    ),
    path(
        "kobo/assets/<str:asset_uid>/",
        KoboAssetDetailAPIView.as_view(),
        name="kobo-asset-detail",
    ),
    path(
        "kobo/assets/<str:asset_uid>/sync/",
        KoboAssetSyncAPIView.as_view(),
        name="kobo-asset-sync",
    ),
    path(
        "kobo/assets/<str:asset_uid>/fetch/",
        KoboAssetRawDataAPIView.as_view(),
        name="kobo-asset-fetch-raw",
    ),
    path(
        "kobo/submissions/",
        KoboSubmissionListAPIView.as_view(),
        name="kobo-submission-list",
    ),
    path(
        "kobo/webhook/",
        KoboRestServiceWebhookAPIView.as_view(),
        name="kobo-rest-service-webhook",
    ),
]

