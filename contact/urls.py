from django.urls import path

from .views import ContactDetailAPIView, ContactListCreateAPIView

urlpatterns = [
    path("contact/", ContactListCreateAPIView.as_view(), name="contact-list-create"),
    path("contact/<int:pk>/", ContactDetailAPIView.as_view(), name="contact-detail"),
]
