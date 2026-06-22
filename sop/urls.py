from django.urls import path

from .views import SOPDetailAPIView, SOPListCreateAPIView

urlpatterns = [
    path("sop/", SOPListCreateAPIView.as_view(), name="sop-list-create"),
    path("sop/<int:pk>/", SOPDetailAPIView.as_view(), name="sop-detail"),
]
