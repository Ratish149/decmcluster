from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name", "is_active")
        extra_kwargs = {
            "email": {"required": True, "allow_blank": False},
            "first_name": {"required": False, "allow_blank": True},
            "last_name": {"required": False, "allow_blank": True},
            "is_active": {"required": False, "default": False},
        }

    def validate_email(self, value):
        if User.objects.filter(
            Q(email__iexact=value) | Q(username__iexact=value)
        ).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        is_active = validated_data.get("is_active", True)
        # Create user with username same as email, and dynamic is_active state
        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            is_active=is_active,
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Find active user by email only
        user = User.objects.filter(email__iexact=email).first()

        if not user:
            raise serializers.ValidationError({
                "non_field_errors": ["Invalid credentials."]
            })

        if not user.check_password(password):
            raise serializers.ValidationError({
                "non_field_errors": ["Invalid Password."]
            })

        if not user.is_active:
            raise serializers.ValidationError({
                "non_field_errors": ["User account is not Verified."]
            })

        # Generate Simple JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Inject custom claims into the access token
        access_token["id"] = user.id
        access_token["username"] = user.username
        access_token["email"] = user.email
        access_token["first_name"] = user.first_name
        access_token["last_name"] = user.last_name
        access_token["is_active"] = user.is_active

        return {
            "refresh": str(refresh),
            "access": str(access_token),
        }


class SuperAdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_superuser",
            "date_joined",
        )
