from django.urls import path

from .views import AdminSOPListAPIView, SOPDetailAPIView, SOPListCreateAPIView

urlpatterns = [
    path("sop/", SOPListCreateAPIView.as_view(), name="sop-list-create"),
    path("sop/admin/", AdminSOPListAPIView.as_view(), name="sop-admin-list"),
    path("sop/<int:pk>/", SOPDetailAPIView.as_view(), name="sop-detail"),
]

