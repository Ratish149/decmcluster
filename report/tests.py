from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from rest_framework.request import Request
from rest_framework.test import APITestCase

from .models import Report, ReportComment
from .serializers import ReportSerializer

User = get_user_model()


class ReportTests(APITestCase):
    def setUp(self):
        self.file = SimpleUploadedFile(
            name="test_report.pdf",
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
    def test_create_report_defaults_and_signal(self, mock_resend_send):
        # Configure Resend settings
        settings.RESEND_API_KEY = "test_api_key"
        settings.DEFAULT_FROM_EMAIL = "from@example.com"
        settings.ADMIN_EMAIL = "admin@example.com"

        mock_resend_send.return_value = {"id": "test_email_id"}

        # Create a new Report
        report = Report.objects.create(
            name="Annual Report 2026", file=self.file, uploaded_by=self.user
        )

        # Assert status defaults to unverified and uploader is set
        assert report.status == Report.StatusChoices.UNVERIFIED
        assert report.uploaded_by == self.user
        assert report.verified_by is None
        assert str(report) == "Annual Report 2026"

        # Assert resend.Emails.send was called due to the post_save signal
        assert mock_resend_send.call_count == 1
        called_args = mock_resend_send.call_args[0][0]
        assert called_args["from"] == "from@example.com"
        assert called_args["to"] == ["admin@example.com"]
        assert "Annual Report 2026" in called_args["subject"]
        assert "testuploader@example.com" in called_args["html"]

    @patch("resend.Emails.send")
    def test_status_filtering(self, mock_resend_send):
        # Create an unverified report
        Report.objects.create(
            name="Unverified Report",
            file=self.file,
            status=Report.StatusChoices.UNVERIFIED,
        )
        # Create a verified report
        Report.objects.create(
            name="Verified Report",
            file=self.file,
            status=Report.StatusChoices.VERIFIED,
        )

        # Verify filtering by status
        unverified = Report.objects.filter(status=Report.StatusChoices.UNVERIFIED)
        assert unverified.count() == 1
        assert unverified.first().name == "Unverified Report"

        verified = Report.objects.filter(status=Report.StatusChoices.VERIFIED)
        assert verified.count() == 1
        assert verified.first().name == "Verified Report"

    def test_comment_required_when_returned_validation(self):
        # If status is RETURNED and comment is empty, should fail validation
        serializer = ReportSerializer(
            data={
                "name": "Returned Test",
                "file": self.file,
                "status": Report.StatusChoices.RETURNED,
                "comment": "",
            }
        )
        assert not serializer.is_valid()
        assert "comment" in serializer.errors

        # If status is RETURNED and comment is provided, should pass validation
        serializer2 = ReportSerializer(
            data={
                "name": "Returned Test 2",
                "file": self.file,
                "status": Report.StatusChoices.RETURNED,
                "comment": "Missing appendix A",
            }
        )
        assert serializer2.is_valid()

    @patch("resend.Emails.send")
    def test_status_update_notifications(self, mock_resend_send):
        settings.RESEND_API_KEY = "test_api_key"
        settings.DEFAULT_FROM_EMAIL = "from@example.com"

        report = Report.objects.create(
            name="Audited Report", file=self.file, uploaded_by=self.user
        )
        # Reset mock call count from initial creation signal
        mock_resend_send.reset_mock()

        # Update status to verified using serializer (simulates API view)
        serializer = ReportSerializer(
            instance=report,
            data={"status": Report.StatusChoices.VERIFIED},
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
        serializer = ReportSerializer(
            instance=report,
            data={
                "status": Report.StatusChoices.RETURNED,
                "comment": "Please scan in higher resolution.",
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
        assert "Please scan in higher resolution." in called_args2["html"]

    @patch("resend.Emails.send")
    def test_reverify_endpoint(self, mock_resend_send):
        settings.RESEND_API_KEY = "test_api_key"
        settings.DEFAULT_FROM_EMAIL = "from@example.com"
        settings.ADMIN_EMAIL = "admin@example.com"

        report = Report.objects.create(
            name="Resubmitted Report",
            file=self.file,
            uploaded_by=self.user,
            status=Report.StatusChoices.RETURNED,
        )
        mock_resend_send.reset_mock()

        self.client.force_authenticate(user=self.user)

        url = f"/api/report/{report.id}/reverify/"
        response = self.client.post(
            url, {"comment": "Here is the higher resolution scan."}
        )

        assert response.status_code == 200
        report.refresh_from_db()

        assert report.status == Report.StatusChoices.UNVERIFIED
        assert report.verified_by is None

        assert report.comments.count() == 1
        latest_comment = report.comments.first()
        assert latest_comment.comment == "Here is the higher resolution scan."
        assert latest_comment.author == self.user

        assert mock_resend_send.call_count == 1
        called_args = mock_resend_send.call_args[0][0]
        assert called_args["to"] == ["admin@example.com"]
        assert "Here is the higher resolution scan." in called_args["html"]

    @patch("resend.Emails.send")
    def test_api_status_update_returned(self, mock_resend_send):
        settings.RESEND_API_KEY = "test_api_key"
        settings.DEFAULT_FROM_EMAIL = "from@example.com"

        report = Report.objects.create(
            name="API Update Report",
            file=self.file,
            uploaded_by=self.user,
            status=Report.StatusChoices.UNVERIFIED,
        )
        mock_resend_send.reset_mock()

        admin_user = User.objects.create_user(
            username="adminuser@example.com",
            email="adminuser@example.com",
            password="securepassword123",
            role="superadmin",
        )
        self.client.force_authenticate(user=admin_user)

        url = f"/api/report/{report.id}/"
        response = self.client.patch(
            url,
            {
                "status": Report.StatusChoices.RETURNED,
                "comment": "Missing appendix A.",
            },
        )

        assert response.status_code == 200
        report.refresh_from_db()

        assert report.status == Report.StatusChoices.RETURNED
        assert report.comments.count() == 1
        latest_comment = report.comments.first()
        assert latest_comment.comment == "Missing appendix A."
        assert latest_comment.author == admin_user

        # Verify that an email was sent via the signals framework
        assert mock_resend_send.call_count == 1
        called_args = mock_resend_send.call_args[0][0]
        assert called_args["to"] == [self.user.email]
        assert "returned" in called_args["subject"].lower()
        assert "Missing appendix A." in called_args["html"]
