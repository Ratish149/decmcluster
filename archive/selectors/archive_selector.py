from typing import Optional

from django.db.models import QuerySet

from archive.models import Archive


def get_archives() -> QuerySet[Archive]:
    """Retrieve all archives ordered by latest created_at."""
    return Archive.objects.all().order_by("-created_at")


def get_archive_by_id(archive_id: int) -> Optional[Archive]:
    """Retrieve a single archive by ID."""
    try:
        return Archive.objects.get(id=archive_id)
    except Archive.DoesNotExist:
        return None
