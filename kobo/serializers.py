from rest_framework import serializers

from kobo.models import KoboAsset, KoboSubmission


class KoboAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = KoboAsset
        fields = [
            "id",
            "name",
            "asset_uid",
            "description",
            "is_active",
            "last_synced_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "last_synced_at",
            "created_at",
            "updated_at",
        ]


class KoboSubmissionSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source="asset.name", read_only=True)
    asset_uid = serializers.CharField(source="asset.asset_uid", read_only=True)

    class Meta:
        model = KoboSubmission
        fields = [
            "id",
            "asset",
            "asset_name",
            "asset_uid",
            "submission_id",
            "data",
            "submitted_at",
            "synced_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "asset",
            "asset_name",
            "asset_uid",
            "submission_id",
            "data",
            "submitted_at",
            "synced_at",
            "created_at",
            "updated_at",
        ]
