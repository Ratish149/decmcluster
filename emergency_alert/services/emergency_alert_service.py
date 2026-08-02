from typing import Any

from django.db import transaction

from emergency_alert.models import EmergencyAlert


class EmergencyAlertService:
    @staticmethod
    @transaction.atomic
    def create_alert(data: dict[str, Any]) -> EmergencyAlert:
        """Create a new emergency alert."""
        alert = EmergencyAlert(**data)
        alert.save()
        return alert

    @staticmethod
    @transaction.atomic
    def update_alert(instance: EmergencyAlert, data: dict[str, Any]) -> EmergencyAlert:
        """Update an existing emergency alert."""
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def delete_alert(instance: EmergencyAlert) -> None:
        """Delete an emergency alert."""
        instance.delete()
