import logging

from django.conf import settings

from decmcluster.services.email_service import send_html_email

logger = logging.getLogger(__name__)


def send_contact_notification_email(contact):
    """
    Sends an HTML email notification to the ADMIN_EMAIL when a new Contact submission is created.
    """
    admin_email = getattr(settings, "ADMIN_EMAIL", None)
    if not admin_email:
        logger.error("ADMIN_EMAIL is not configured in settings. Skipping contact notification email.")
        return False

    subject = f"New Contact Submission from {contact.full_name}"
    context = {
        "full_name": contact.full_name,
        "email": contact.email or "N/A",
        "phone": contact.phone or "N/A",
        "message": contact.message,
        "created_at": contact.created_at,
    }

    return send_html_email(
        subject=subject,
        to_email=admin_email,
        template_name="emails/contact_notification.html",
        context=context,
    )
