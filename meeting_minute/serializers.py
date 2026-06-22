from rest_framework import serializers

from .models import MeetingMinute


class MeetingMinuteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingMinute
        fields = [
            "id",
            "name",
            "file",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
