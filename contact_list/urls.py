from django.urls import path

from .views import ContactListDetailAPIView, ContactListListCreateAPIView

urlpatterns = [
    path(
        "contact-list/",
        ContactListListCreateAPIView.as_view(),
        name="contact-list-list-create",
    ),
    path(
        "contact-list/<int:pk>/",
        ContactListDetailAPIView.as_view(),
        name="contact-list-detail",
    ),
]
