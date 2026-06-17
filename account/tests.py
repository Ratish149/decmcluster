import jwt
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAuthTests(APITestCase):
    def setUp(self):
        # Create an active user for testing login
        self.active_user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="securepassword123",
            is_active=True,
        )
        # Create an inactive user
        self.inactive_user = User.objects.create_user(
            username="inactive@example.com",
            email="inactive@example.com",
            password="securepassword123",
            is_active=False,
        )
        # Create a superadmin user
        self.superadmin = User.objects.create_superuser(
            username="superadmin@example.com",
            email="superadmin@example.com",
            password="superpassword123",
        )

        self.login_url = reverse("login")
        self.register_url = reverse("register")

    def test_registration_success(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.register_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"]["username"] == "newuser@example.com"
        assert response.data["user"]["email"] == "newuser@example.com"
        assert response.data["user"]["is_active"] is False

        # Verify database record
        user = User.objects.get(email="newuser@example.com")
        assert user.username == "newuser@example.com"
        assert user.is_active is False
        assert user.check_password("newpassword123")

    def test_registration_duplicate_email(self):
        data = {
            "email": "testuser@example.com",  # existing email
            "password": "password123",
        }
        response = self.client.post(self.register_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_login_success_with_email(self):
        data = {"email": "testuser@example.com", "password": "securepassword123"}
        response = self.client.post(self.login_url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

        # Decode access token to verify custom claims
        access_token = response.data["access"]
        decoded_payload = jwt.decode(access_token, options={"verify_signature": False})
        assert decoded_payload["id"] == self.active_user.id
        assert decoded_payload["email"] == "testuser@example.com"
        assert decoded_payload["username"] == "testuser@example.com"
        assert decoded_payload["is_active"] is True

    def test_login_failure_invalid_email_format(self):
        # Trying to login using a non-email format string should trigger field validation error
        data = {"email": "testuser", "password": "securepassword123"}
        response = self.client.post(self.login_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_login_failure_non_existent_email(self):
        # Trying to login with a non-existent email should fail authentication validation
        data = {"email": "nonexistent@example.com", "password": "securepassword123"}
        response = self.client.post(self.login_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data
        assert response.data["non_field_errors"][0] == "Invalid credentials."

    def test_login_failure_inactive_user(self):
        data = {"email": "inactive@example.com", "password": "securepassword123"}
        response = self.client.post(self.login_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data
        assert response.data["non_field_errors"][0] == "User account is not Verified."

    def test_login_failure_wrong_password(self):
        data = {"email": "testuser@example.com", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data
        assert response.data["non_field_errors"][0] == "Invalid Password."

    def test_superuser_verify_success(self):
        # Authenticate client as superuser
        self.client.force_authenticate(user=self.superadmin)
        url = reverse("superuser-verify", kwargs={"pk": self.inactive_user.pk})

        response = self.client.patch(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["user"]["is_active"] is True

        # Verify db status
        self.inactive_user.refresh_from_db()
        assert self.inactive_user.is_active is True

    def test_superuser_verify_unauthorized_non_superuser(self):
        # Authenticate client as regular user
        self.client.force_authenticate(user=self.active_user)
        url = reverse("superuser-verify", kwargs={"pk": self.inactive_user.pk})

        response = self.client.patch(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "detail" in response.data

    def test_superuser_verify_unauthenticated(self):
        # Do not authenticate client
        url = reverse("superuser-verify", kwargs={"pk": self.inactive_user.pk})

        response = self.client.patch(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_superuser_verify_already_active(self):
        self.client.force_authenticate(user=self.superadmin)
        url = reverse("superuser-verify", kwargs={"pk": self.active_user.pk})

        response = self.client.patch(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.data

    def test_superuser_verify_non_existent_user(self):
        self.client.force_authenticate(user=self.superadmin)
        url = reverse("superuser-verify", kwargs={"pk": 99999})

        response = self.client.patch(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "detail" in response.data

    def test_superuser_get_users_list_success(self):
        self.client.force_authenticate(user=self.superadmin)
        url = reverse("superuser-user-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_superuser_get_users_list_unauthorized_non_superuser(self):
        self.client.force_authenticate(user=self.active_user)
        url = reverse("superuser-user-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_superuser_get_users_list_unauthenticated(self):
        url = reverse("superuser-user-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_superuser_get_user_detail_success(self):
        self.client.force_authenticate(user=self.superadmin)
        url = reverse("superuser-user-detail", kwargs={"pk": self.active_user.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == self.active_user.email
        assert response.data["username"] == self.active_user.username

    def test_superuser_get_user_detail_unauthorized_non_superuser(self):
        self.client.force_authenticate(user=self.active_user)
        url = reverse("superuser-user-detail", kwargs={"pk": self.inactive_user.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_superuser_get_user_detail_unauthenticated(self):
        url = reverse("superuser-user-detail", kwargs={"pk": self.inactive_user.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_superuser_get_user_detail_not_found(self):
        self.client.force_authenticate(user=self.superadmin)
        url = reverse("superuser-user-detail", kwargs={"pk": 99999})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_superuser_create_user_success(self):
        self.client.force_authenticate(user=self.superadmin)
        url = reverse("superuser-user-list")
        data = {
            "email": "createdbysuperadmin@example.com",
            "password": "createdpassword123",
            "first_name": "Created",
            "last_name": "Admin",
            "is_active": True,
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == "createdbysuperadmin@example.com"
        assert response.data["is_active"] is True

        # Verify db status
        user = User.objects.get(email="createdbysuperadmin@example.com")
        assert user.is_active is True
        assert user.check_password("createdpassword123")

    def test_superuser_update_user_success(self):
        self.client.force_authenticate(user=self.superadmin)
        url = reverse("superuser-user-detail", kwargs={"pk": self.active_user.pk})
        data = {
            "first_name": "UpdatedName",
            "last_name": "UpdatedLastName",
        }
        response = self.client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "UpdatedName"
        assert response.data["last_name"] == "UpdatedLastName"

        self.active_user.refresh_from_db()
        assert self.active_user.first_name == "UpdatedName"

    def test_superuser_delete_user_success(self):
        self.client.force_authenticate(user=self.superadmin)
        url = reverse("superuser-user-detail", kwargs={"pk": self.active_user.pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not User.objects.filter(pk=self.active_user.pk).exists()

