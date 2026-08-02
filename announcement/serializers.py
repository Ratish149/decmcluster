from django.utils.text import slugify
from rest_framework import serializers

from .models import Announcement
from .services.announcement_service import AnnouncementService


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
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
            qs = Announcement.objects.filter(slug=slug)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"title": "An announcement with this title/slug already exists."}
                )
            attrs["slug"] = slug
        return attrs

    def create(self, validated_data):
        return AnnouncementService.create_announcement(validated_data)

    def update(self, instance, validated_data):
        return AnnouncementService.update_announcement(instance, validated_data)
