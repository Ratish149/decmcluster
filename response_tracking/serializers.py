from rest_framework import serializers

from .models import ResponseTracking


class ResponseTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseTracking
        fields = [
            "id",
            "name",
            "file",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
