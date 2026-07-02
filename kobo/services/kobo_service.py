from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kobo.models import KoboWebhookLog

import logging

import requests
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from kobo.models import KoboAsset, KoboSubmission

logger = logging.getLogger(__name__)


class KoboService:
    """
    Service class to handle all API operations with KoboToolbox.
    """

    def __init__(self):
        self.api_key = getattr(settings, "KOBO_API_KEY", None)
        self.base_url = getattr(
            settings, "KOBO_BASE_URL", "https://kf.kobotoolbox.org"
        ).rstrip("/")

        if not self.api_key:
            logger.warning("KOBO_API_KEY is not configured in settings.")

    def _get_headers(self):
        if not self.api_key:
            raise ValueError(
                "KoboToolbox API token is not configured. Please add KOBO_API_KEY to your environment/settings."
            )
        return {
            "Authorization": f"Token {self.api_key}",
            "Accept": "application/json",
        }

    def fetch_assets(self):
        """
        Fetches the list of all forms/projects (assets) from KoboToolbox.
        """
        url = f"{self.base_url}/api/v2/assets/?format=json"
        headers = self._get_headers()

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("results", [])

    def sync_registered_assets(self):
        """
        Pulls all assets from Kobo and registers/updates them in the local database.
        Note: This only registers the assets themselves, not their submissions.
        """
        assets_data = self.fetch_assets()
        synced_assets = []

        with transaction.atomic():
            for data in assets_data:
                # We only want 'survey' type assets (forms)
                if data.get("asset_type") != "survey":
                    continue

                asset, created = KoboAsset.objects.update_or_create(
                    asset_uid=data.get("uid"),
                    defaults={
                        "name": data.get("name", ""),
                        "description": data.get("settings", {}).get("description", "")
                        or "",
                    },
                )
                synced_assets.append(asset)

        return synced_assets

    def sync_submissions(self, asset_uid):
        """
        Synchronizes all submissions for a given asset UID from KoboToolbox to local DB.
        """
        try:
            asset = KoboAsset.objects.get(asset_uid=asset_uid)
        except KoboAsset.DoesNotExist:
            raise ValueError(
                f"Asset with UID {asset_uid} is not registered in the database."
            )

        url = f"{self.base_url}/api/v2/assets/{asset_uid}/data/?format=json"
        headers = self._get_headers()
        sync_count = 0

        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            res_data = response.json()

            submissions_list = res_data.get("results", [])

            with transaction.atomic():
                for sub_data in submissions_list:
                    sub_id = sub_data.get("_id")
                    sub_time_str = sub_data.get("_submission_time")

                    if not sub_id:
                        continue

                    # Parse submission time or fallback to current time
                    submitted_at = (
                        parse_datetime(sub_time_str) if sub_time_str else timezone.now()
                    )

                    # Update or create the submission in the local DB
                    _, created = KoboSubmission.objects.update_or_create(
                        submission_id=sub_id,
                        defaults={
                            "asset": asset,
                            "data": sub_data,
                            "submitted_at": submitted_at,
                        },
                    )
                    if created:
                        sync_count += 1

            # Follow pagination if available
            url = res_data.get("next")

        # Update last synced timestamp
        asset.last_synced_at = timezone.now()
        asset.save(update_fields=["last_synced_at"])

        return sync_count

    def fetch_raw_submissions(self, asset_uid):
        """
        Directly fetches raw submissions data from KoboToolbox for a specific asset UID.
        """
        url = f"{self.base_url}/api/v2/assets/{asset_uid}/data/?format=json"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def handle_webhook_payload(self, payload: dict) -> KoboWebhookLog:
        """
        Parses and stores the raw webhook payload from KoboToolbox REST Service.
        Called whenever KoboToolbox pushes a new submission to our endpoint.
        """
        from kobo.models import KoboWebhookLog

        sub_id = payload.get("_id")
        uuid = payload.get("_uuid", "")
        asset_uid = payload.get("_xform_id_string", "")
        submission_time_str = payload.get("_submission_time")
        submitted_at = (
            parse_datetime(submission_time_str) if submission_time_str else None
        )

        log = KoboWebhookLog.objects.create(
            asset_uid=asset_uid,
            submission_id=sub_id,
            uuid=uuid,
            payload=payload,
            submission_time=submitted_at,
        )

        logger.info(
            "Webhook received: asset_uid=%s submission_id=%s uuid=%s",
            asset_uid,
            sub_id,
            uuid,
        )
        return log
