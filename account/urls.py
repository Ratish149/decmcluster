from django.urls import path

from .views import (
    SuperAdminUserDetailAPIView,
    SuperAdminUserListAPIView,
    SuperAdminUserVerifyAPIView,
    UserLoginAPIView,
    UserRegistrationAPIView,
)

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path(
        "verify/<int:pk>/",
        SuperAdminUserVerifyAPIView.as_view(),
        name="superuser-verify",
    ),
    path("users/", SuperAdminUserListAPIView.as_view(), name="superuser-user-list"),
    path(
        "users/<int:pk>/",
        SuperAdminUserDetailAPIView.as_view(),
        name="superuser-user-detail",
    ),
]
