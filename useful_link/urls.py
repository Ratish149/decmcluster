from django.urls import path

from .views import UsefulLinkDetailAPIView, UsefulLinkListCreateAPIView

urlpatterns = [
    path(
        "useful-link/",
        UsefulLinkListCreateAPIView.as_view(),
        name="useful-link-list-create",
    ),
    path(
        "useful-link/<int:pk>/",
        UsefulLinkDetailAPIView.as_view(),
        name="useful-link-detail",
    ),
]
