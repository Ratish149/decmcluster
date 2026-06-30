from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import MeetingMinute, MeetingMinuteComment

User = get_user_model()


class UserMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role"]


class MeetingMinuteCommentSerializer(serializers.ModelSerializer):
    author = UserMinSerializer(read_only=True)

    class Meta:
        model = MeetingMinuteComment
        fields = ["id", "author", "comment", "created_at"]


class MeetingMinuteSerializer(serializers.ModelSerializer):
    uploaded_by = UserMinSerializer(read_only=True)
    verified_by = UserMinSerializer(read_only=True)
    comments = MeetingMinuteCommentSerializer(many=True, read_only=True)
    comment = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = MeetingMinute
        fields = [
            "id",
            "name",
            "file",
            "status",
            "comments",
            "comment",
            "uploaded_by",
            "verified_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "uploaded_by",
            "verified_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        status = attrs.get("status")
        if not status and self.instance:
            status = self.instance.status
        comment = attrs.get("comment")

        if status == MeetingMinute.StatusChoices.RETURNED:
            has_existing = (
                self.instance and self.instance.comments.exists()
                if self.instance
                else False
            )
            if not comment and not has_existing:
                raise serializers.ValidationError({
                    "comment": "Comment is required when returning a meeting minute."
                })
        return attrs

    def create(self, validated_data):
        comment_value = validated_data.pop("comment", None)
        instance = super().create(validated_data)
        if comment_value:
            request = self.context.get("request")
            author = request.user if request and request.user.is_authenticated else None
            MeetingMinuteComment.objects.create(
                meeting_minute=instance,
                author=author,
                comment=comment_value,
            )
        return instance

    def update(self, instance, validated_data):
        comment_value = validated_data.pop("comment", None)
        # Create comment first so it is available in pre_save/post_save signals on instance.save()
        if comment_value:
            request = self.context.get("request")
            author = request.user if request and request.user.is_authenticated else None
            MeetingMinuteComment.objects.create(
                meeting_minute=instance,
                author=author,
                comment=comment_value,
            )
        return super().update(instance, validated_data)
