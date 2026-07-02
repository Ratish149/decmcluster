from django.db import models


class KoboAsset(models.Model):
    name = models.CharField(max_length=255)
    asset_uid = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "last_synced_at"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.asset_uid})"


class KoboSubmission(models.Model):
    asset = models.ForeignKey(
        KoboAsset,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    # Kobo uses an integer ID for submissions (e.g. `_id`), using BigIntegerField is safest.
    submission_id = models.BigIntegerField(unique=True, db_index=True)
    data = models.JSONField()
    submitted_at = models.DateTimeField(db_index=True)
    synced_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_at"]
        indexes = [
            models.Index(fields=["asset", "submitted_at"]),
        ]

    def __str__(self):
        return f"Submission {self.submission_id} for {self.asset.name}"


class KoboWebhookLog(models.Model):
    """
    Stores raw payloads received from KoboToolbox REST Service webhooks.
    Created automatically whenever KoboToolbox pushes a new submission to our endpoint.
    """

    asset_uid = models.CharField(max_length=100, db_index=True, blank=True, default="")
    submission_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    uuid = models.CharField(max_length=100, blank=True, default="", db_index=True)
    payload = models.JSONField()
    submission_time = models.DateTimeField(null=True, blank=True, db_index=True)
    received_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-received_at"]
        indexes = [
            models.Index(fields=["asset_uid", "received_at"]),
        ]

    def __str__(self):
        return f"Webhook [{self.asset_uid}] submission {self.submission_id} at {self.received_at}"
