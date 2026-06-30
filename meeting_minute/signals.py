from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from decmcluster.services.email_service import send_status_update_email

from .models import MeetingMinute
from .utils import send_meeting_minute_verification_email


@receiver(pre_save, sender=MeetingMinute)
def capture_old_status(sender, instance, **kwargs):
    """
    Pre-save receiver to capture the status of the MeetingMinute before saving.
    """
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except sender.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=MeetingMinute)
def send_status_change_email(sender, instance, created, **kwargs):
    """
    Post-save receiver to send email notifications:
    - Admin verification email when created.
    - Uploader notification email when status changes.
    """
    if created:
        send_meeting_minute_verification_email(instance)
        return

    old_status = getattr(instance, "_old_status", None)
    if old_status and instance.status != old_status:
        # Check if the status has transitioned to verified or returned
        if instance.status in (
            MeetingMinute.StatusChoices.VERIFIED,
            MeetingMinute.StatusChoices.RETURNED,
        ):
            comment_text = None
            if instance.status == MeetingMinute.StatusChoices.RETURNED:
                from .models import MeetingMinuteComment
                latest_comment = MeetingMinuteComment.objects.filter(meeting_minute=instance).order_by("-created_at").first()
                if latest_comment:
                    comment_text = latest_comment.comment

            send_status_update_email(
                instance=instance,
                model_name="Meeting Minute",
                new_status=instance.status,
                comment=comment_text,
            )
