from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from rest_framework.request import Request
from rest_framework.test import APITestCase

from .models import SOP, SOPComment
from .serializers import SOPSerializer

User = get_user_model()


class SOPTests(APITestCase):
    def setUp(self):
        self.file = SimpleUploadedFile(
            name="test_sop.pdf",
            content=b"Dummy content",
            content_type="application/pdf",
        )
        self.user = User.objects.create_user(
            username="testuploader@example.com",
            email="testuploader@example.com",
            password="securepassword123",
        )
        self.verifier = User.objects.create_user(
            username="testverifier@example.com",
            email="testverifier@example.com",
            password="securepassword123",
        )

    @patch("resend.Emails.send")
    def test_create_sop_defaults_and_signal(self, mock_resend_send):
        # Configure Resend settings
        settings.RESEND_API_KEY = "test_api_key"
        settings.DEFAULT_FROM_EMAIL = "from@example.com"
        settings.ADMIN_EMAIL = "admin@example.com"

        mock_resend_send.return_value = {"id": "test_email_id"}

        # Create a new SOP
        sop = SOP.objects.create(
            name="Emergency Response SOP", file=self.file, uploaded_by=self.user
        )

        # Assert status defaults to unverified and uploader is set
        assert sop.status == SOP.StatusChoices.UNVERIFIED
        assert sop.uploaded_by == self.user
        assert sop.verified_by is None
        assert str(sop) == "Emergency Response SOP"

        # Assert resend.Emails.send was called due to the post_save signal
        assert mock_resend_send.call_count == 1
        called_args = mock_resend_send.call_args[0][0]
        assert called_args["from"] == "from@example.com"
        assert called_args["to"] == ["admin@example.com"]
        assert "Emergency Response SOP" in called_args["subject"]
        assert "testuploader@example.com" in called_args["html"]

    @patch("resend.Emails.send")
    def test_status_filtering(self, mock_resend_send):
        # Create an unverified SOP
        SOP.objects.create(
            name="Unverified SOP",
            file=self.file,
            status=SOP.StatusChoices.UNVERIFIED,
        )
        # Create a verified SOP
        SOP.objects.create(
            name="Verified SOP",
            file=self.file,
            status=SOP.StatusChoices.VERIFIED,
        )

        # Verify filtering by status
        unverified = SOP.objects.filter(status=SOP.StatusChoices.UNVERIFIED)
        assert unverified.count() == 1
        assert unverified.first().name == "Unverified SOP"

        verified = SOP.objects.filter(status=SOP.StatusChoices.VERIFIED)
        assert verified.count() == 1
        assert verified.first().name == "Verified SOP"

    def test_comment_required_when_returned_validation(self):
        # If status is RETURNED and comment is empty, should fail validation
        serializer = SOPSerializer(
            data={
                "name": "Returned Test",
                "file": self.file,
                "status": SOP.StatusChoices.RETURNED,
                "comment": "",
            }
        )
        assert not serializer.is_valid()
        assert "comment" in serializer.errors

        # If status is RETURNED and comment is provided, should pass validation
        serializer2 = SOPSerializer(
            data={
                "name": "Returned Test 2",
                "file": self.file,
                "status": SOP.StatusChoices.RETURNED,
                "comment": "Missing detail on page 3",
            }
        )
        assert serializer2.is_valid()

    @patch("resend.Emails.send")
    def test_status_update_notifications(self, mock_resend_send):
        settings.RESEND_API_KEY = "test_api_key"
        settings.DEFAULT_FROM_EMAIL = "from@example.com"

        sop = SOP.objects.create(
            name="Audited SOP", file=self.file, uploaded_by=self.user
        )
        # Reset mock call count from initial creation signal
        mock_resend_send.reset_mock()

        # Update status to verified using serializer (simulates API view)
        serializer = SOPSerializer(
            instance=sop,
            data={"status": SOP.StatusChoices.VERIFIED},
            partial=True,
        )
        assert serializer.is_valid()
        serializer.save(verified_by=self.verifier)

        # Assert email was sent automatically via signals
        assert mock_resend_send.call_count == 1
        called_args = mock_resend_send.call_args[0][0]
        assert called_args["to"] == [self.user.email]
        assert "verified" in called_args["subject"].lower()
        assert "verified" in called_args["html"].lower()

        # Reset mock
        mock_resend_send.reset_mock()

        # Update status to returned with comment
        serializer = SOPSerializer(
            instance=sop,
            data={
                "status": SOP.StatusChoices.RETURNED,
                "comment": "Please describe Section 2.1 in more detail.",
            },
            partial=True,
        )
        # Add request context to serializer for author attribution
        factory = RequestFactory()
        django_request = factory.put("/")
        django_request.user = self.verifier
        serializer.context["request"] = Request(django_request)

        assert serializer.is_valid()
        serializer.save()

        # Assert email was sent automatically via signals
        assert mock_resend_send.call_count == 1
        called_args2 = mock_resend_send.call_args[0][0]
        assert called_args2["to"] == [self.user.email]
        assert "returned" in called_args2["subject"].lower()
        assert "Please describe Section 2.1 in more detail." in called_args2["html"]

    @patch("resend.Emails.send")
    def test_reverify_endpoint(self, mock_resend_send):
        settings.RESEND_API_KEY = "test_api_key"
        settings.DEFAULT_FROM_EMAIL = "from@example.com"
        settings.ADMIN_EMAIL = "admin@example.com"

        sop = SOP.objects.create(
            name="Resubmitted SOP",
            file=self.file,
            uploaded_by=self.user,
            status=SOP.StatusChoices.RETURNED,
        )
        mock_resend_send.reset_mock()

        self.client.force_authenticate(user=self.user)

        url = f"/api/sop/{sop.id}/reverify/"
        response = self.client.post(
            url, {"comment": "Added the requested detail to section 2.1."}
        )

        assert response.status_code == 200
        sop.refresh_from_db()

        assert sop.status == SOP.StatusChoices.UNVERIFIED
        assert sop.verified_by is None

        assert sop.comments.count() == 1
        latest_comment = sop.comments.first()
        assert latest_comment.comment == "Added the requested detail to section 2.1."
        assert latest_comment.author == self.user

        assert mock_resend_send.call_count == 1
        called_args = mock_resend_send.call_args[0][0]
        assert called_args["to"] == ["admin@example.com"]
        assert "Added the requested detail to section 2.1." in called_args["html"]

    @patch("resend.Emails.send")
    def test_api_status_update_returned(self, mock_resend_send):
        settings.RESEND_API_KEY = "test_api_key"
        settings.DEFAULT_FROM_EMAIL = "from@example.com"

        sop = SOP.objects.create(
            name="API Update SOP",
            file=self.file,
            uploaded_by=self.user,
            status=SOP.StatusChoices.UNVERIFIED,
        )
        mock_resend_send.reset_mock()

        admin_user = User.objects.create_user(
            username="adminuser@example.com",
            email="adminuser@example.com",
            password="securepassword123",
            role="superadmin",
        )
        self.client.force_authenticate(user=admin_user)

        url = f"/api/sop/{sop.id}/"
        response = self.client.patch(
            url,
            {
                "status": SOP.StatusChoices.RETURNED,
                "comment": "Need to clarify target audience.",
            },
        )

        assert response.status_code == 200
        sop.refresh_from_db()

        assert sop.status == SOP.StatusChoices.RETURNED
        assert sop.comments.count() == 1
        latest_comment = sop.comments.first()
        assert latest_comment.comment == "Need to clarify target audience."
        assert latest_comment.author == admin_user

        # Verify that an email was sent via the signals framework
        assert mock_resend_send.call_count == 1
        called_args = mock_resend_send.call_args[0][0]
        assert called_args["to"] == [self.user.email]
        assert "returned" in called_args["subject"].lower()
        assert "Need to clarify target audience." in called_args["html"]
