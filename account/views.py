from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import UserFilter
from .serializers import (
    SuperAdminUserSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)

User = get_user_model()


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully. Please check your email to verify your account.",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEmailVerificationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        if not token:
            return Response(
                {"detail": "Token is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        from account.services.verification_service import verify_token_and_get_user

        user = verify_token_and_get_user(token)

        if not user:
            return Response(
                {"detail": "Invalid or expired verification token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_active:
            return Response(
                {"message": "Email is already verified.", "email": user.email},
                status=status.HTTP_200_OK,
            )

        user.is_active = True
        user.save()

        return Response(
            {"message": "Email verified successfully.", "email": user.email},
            status=status.HTTP_200_OK,
        )


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuperAdminUserVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def patch(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if user.is_active:
            return Response(
                {"detail": "User is already active/verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = True
        user.save()

        return Response(
            {
                "message": "User verified successfully.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "is_active": user.is_active,
                },
            },
            status=status.HTTP_200_OK,
        )


class SuperAdminUserListAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    queryset = User.objects.all().order_by("-id")
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = UserFilter
    search_fields = ["email", "first_name", "last_name"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserRegistrationSerializer
        return SuperAdminUserSerializer

    def perform_create(self, serializer):
        serializer.save()


class SuperAdminUserDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    queryset = User.objects.all()
    serializer_class = SuperAdminUserSerializer
