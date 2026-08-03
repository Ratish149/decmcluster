from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Contact
from .services.contact_service import send_contact_notification_email


@receiver(post_save, sender=Contact)
def send_contact_admin_email_on_creation(sender, instance, created, **kwargs):
    """
    Post-save signal receiver to automatically send an email notification
    to the admin whenever a new Contact message is created.
    """
    if created:
        send_contact_notification_email(instance)
