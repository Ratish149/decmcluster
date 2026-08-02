from django.template.defaultfilters import slugify
from rest_framework import serializers

from .models import EmergencyAlert
from .services.emergency_alert_service import EmergencyAlertService


class EmergencyAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyAlert
        fields = [
            "id",
            "title",
            "slug",
            "link",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def validate(self, attrs):
        title = attrs.get("title", self.instance.title if self.instance else None)
        if title:
            slug = slugify(title)
            qs = EmergencyAlert.objects.filter(slug=slug)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"title": "An emergency alert with this title/slug already exists."}
                )
            attrs["slug"] = slug
        return attrs

    def create(self, validated_data):
        return EmergencyAlertService.create_alert(validated_data)

    def update(self, instance, validated_data):
        return EmergencyAlertService.update_alert(instance, validated_data)
