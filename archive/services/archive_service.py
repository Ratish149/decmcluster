from typing import Any

from django.db import transaction

from archive.models import Archive


class ArchiveService:
    @staticmethod
    @transaction.atomic
    def create_archive(data: dict[str, Any]) -> Archive:
        """Create a new archive."""
        archive = Archive(**data)
        archive.save()
        return archive

    @staticmethod
    @transaction.atomic
    def update_archive(instance: Archive, data: dict[str, Any]) -> Archive:
        """Update an existing archive."""
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def delete_archive(instance: Archive) -> None:
        """Delete an archive."""
        instance.delete()
