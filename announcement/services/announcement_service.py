from typing import Any

from django.db import transaction

from announcement.models import Announcement


class AnnouncementService:
    @staticmethod
    @transaction.atomic
    def create_announcement(data: dict[str, Any]) -> Announcement:
        """Create a new announcement."""
        announcement = Announcement(**data)
        announcement.save()
        return announcement

    @staticmethod
    @transaction.atomic
    def update_announcement(
        instance: Announcement, data: dict[str, Any]
    ) -> Announcement:
        """Update an existing announcement."""
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def delete_announcement(instance: Announcement) -> None:
        """Delete an announcement."""
        instance.delete()
