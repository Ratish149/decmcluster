from typing import Optional

from django.db.models import QuerySet

from announcement.models import Announcement


def get_announcements() -> QuerySet[Announcement]:
    """Retrieve all announcements optimized and ordered by latest created_at."""
    return Announcement.objects.all().order_by("-created_at")


def get_announcement_by_slug(slug: str) -> Optional[Announcement]:
    """Retrieve a single announcement by slug."""
    try:
        return Announcement.objects.get(slug=slug)
    except Announcement.DoesNotExist:
        return None
