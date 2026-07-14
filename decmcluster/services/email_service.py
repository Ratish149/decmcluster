import logging

import resend
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_html_email(subject, to_email, template_name, context):
    """
    Renders an HTML template and sends it using Resend SDK.
    """
    api_key = getattr(settings, "RESEND_API_KEY", None)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)

    if not api_key:
        logger.error("RESEND_API_KEY is not configured in settings.")
        return False
    if not from_email:
        logger.error("DEFAULT_FROM_EMAIL is not configured in settings.")
        return False

    resend.api_key = api_key

    try:
        html_content = render_to_string(template_name, context)
    except Exception as e:
        logger.exception(f"Error rendering template {template_name}: {e}")
        return False

    params = {
        "from": from_email,
        "to": [to_email] if isinstance(to_email, str) else to_email,
        "subject": subject,
        "html": html_content,
    }

    try:
        response = resend.Emails.send(params)
        print("email sent successfully")
        logger.info(
            f"Email sent successfully. Subject: {subject}. Response: {response}"
        )
        return True
    except Exception as e:
        logger.exception(f"Error sending email via Resend: {e}")
        return False


def send_model_verification_email(
    instance, model_name, details, admin_email=None, admin_url=None
):
    """
    Standardized function to send a verification email to the admin for any model creation.
    """
    if not admin_email:
        admin_email = getattr(settings, "ADMIN_EMAIL", None)

    if not admin_email:
        logger.error("ADMIN_EMAIL is not configured in settings.")
        return False

    if not admin_url:
        admin_url = getattr(
            settings, "ADMIN_URL", "https://decmcluster.org/verify-content/"
        )

    subject = f"Verification Required: New {model_name} Created."
    context = {
        "model_name": model_name,
        "instance_name": str(instance),
        "instance_status": instance.status.capitalize(),
        "details": details,
        "admin_url": admin_url,
    }
    print("email sent to", admin_email)

    return send_html_email(
        subject=subject,
        to_email=admin_email,
        template_name="emails/verification.html",
        context=context,
    )


def send_status_update_email(instance, model_name, new_status, comment=None):
    """
    Sends a notification email to the uploader when a model status changes.
    """
    print("Email sending for veification")
    if not instance.uploaded_by or not instance.uploaded_by.email:
        logger.warning(
            f"No uploader or uploader email found for {model_name} {instance.id}. Skipping email."
        )
        return False

    to_email = instance.uploaded_by.email
    print("uploaded by", to_email)
    instance_name = str(instance)

    if new_status == "verified":
        subject = f"Verified: Your {model_name} has been verified."
        template_name = "emails/verified.html"
        context = {
            "model_name": model_name,
            "instance_name": instance_name,
        }
    elif new_status == "returned":
        subject = f"Action Required: Your {model_name} was returned."
        template_name = "emails/returned.html"
        base_url = getattr(settings, "ADMIN_URL", "http://192.168.1.80:3000/")
        if not base_url.endswith("/"):
            base_url += "/"

        # Build edit url dynamically based on model name
        model_path = model_name.lower().replace(" ", "-")
        edit_url = f"{base_url}{model_path}/edit/{instance.id}/"

        context = {
            "model_name": model_name,
            "instance_name": instance_name,
            "comment": comment
            or getattr(instance, "comment", "")
            or "No comment provided.",
            "edit_url": edit_url,
        }
    else:
        logger.warning(f"No email flow defined for status: {new_status}")
        return False

    return send_html_email(
        subject=subject,
        to_email=to_email,
        template_name=template_name,
        context=context,
    )
