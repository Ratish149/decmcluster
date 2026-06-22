from django.urls import path

from .views import TrainingDetailAPIView, TrainingListCreateAPIView

urlpatterns = [
    path("training/", TrainingListCreateAPIView.as_view(), name="training-list-create"),
    path("training/<int:pk>/", TrainingDetailAPIView.as_view(), name="training-detail"),
]
