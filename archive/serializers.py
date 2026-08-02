from rest_framework import serializers

from .models import Archive
from .services.archive_service import ArchiveService


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = [
            "id",
            "survey_type",
            "date",
            "survery_tools",
            "level",
            "file",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        return ArchiveService.create_archive(validated_data)

    def update(self, instance, validated_data):
        return ArchiveService.update_archive(instance, validated_data)
