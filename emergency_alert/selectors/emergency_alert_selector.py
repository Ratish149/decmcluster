from typing import Optional

from django.db.models import QuerySet

from emergency_alert.models import EmergencyAlert


def get_emergency_alerts() -> QuerySet[EmergencyAlert]:
    """Retrieve all emergency alerts optimized and ordered by latest created_at."""
    return EmergencyAlert.objects.all().order_by("-created_at")


def get_emergency_alert_by_slug(slug: str) -> Optional[EmergencyAlert]:
    """Retrieve a single emergency alert by slug."""
    try:
        return EmergencyAlert.objects.get(slug=slug)
    except EmergencyAlert.DoesNotExist:
        return None
