from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Report, ReportComment

User = get_user_model()


class UserMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role"]


class ReportCommentSerializer(serializers.ModelSerializer):
    author = UserMinSerializer(read_only=True)

    class Meta:
        model = ReportComment
        fields = ["id", "author", "comment", "created_at"]


class ReportSerializer(serializers.ModelSerializer):
    uploaded_by = UserMinSerializer(read_only=True)
    verified_by = UserMinSerializer(read_only=True)
    comments = ReportCommentSerializer(many=True, read_only=True)
    comment = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Report
        fields = [
            "id",
            "name",
            "image",
            "file",
            "type",
            "url",
            "date",
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

        if status == Report.StatusChoices.RETURNED:
            has_existing = (
                self.instance and self.instance.comments.exists()
                if self.instance
                else False
            )
            if not comment and not has_existing:
                raise serializers.ValidationError({
                    "comment": "Comment is required when returning a report."
                })
        return attrs

    def create(self, validated_data):
        comment_value = validated_data.pop("comment", None)
        instance = super().create(validated_data)
        if comment_value:
            request = self.context.get("request")
            author = request.user if request and request.user.is_authenticated else None
            ReportComment.objects.create(
                report=instance,
                author=author,
                comment=comment_value,
            )
        return instance

    def update(self, instance, validated_data):
        comment_value = validated_data.pop("comment", None)
        if comment_value:
            request = self.context.get("request")
            author = request.user if request and request.user.is_authenticated else None
            ReportComment.objects.create(
                report=instance,
                author=author,
                comment=comment_value,
            )
        return super().update(instance, validated_data)


class AdminReportSerializer(serializers.ModelSerializer):
    uploaded_by = UserMinSerializer(read_only=True)
    verified_by = UserMinSerializer(read_only=True)
    comments = ReportCommentSerializer(many=True, read_only=True)
    comment = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Report
        fields = [
            "id",
            "name",
            "image",
            "file",
            "type",
            "url",
            "date",
            "is_situation_report",
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

        if status == Report.StatusChoices.RETURNED:
            has_existing = (
                self.instance and self.instance.comments.exists()
                if self.instance
                else False
            )
            if not comment and not has_existing:
                raise serializers.ValidationError({
                    "comment": "Comment is required when returning a report."
                })
        return attrs

    def create(self, validated_data):
        comment_value = validated_data.pop("comment", None)
        instance = super().create(validated_data)
        if comment_value:
            request = self.context.get("request")
            author = request.user if request and request.user.is_authenticated else None
            ReportComment.objects.create(
                report=instance,
                author=author,
                comment=comment_value,
            )
        return instance

    def update(self, instance, validated_data):
        comment_value = validated_data.pop("comment", None)
        if comment_value:
            request = self.context.get("request")
            author = request.user if request and request.user.is_authenticated else None
            ReportComment.objects.create(
                report=instance,
                author=author,
                comment=comment_value,
            )
        return super().update(instance, validated_data)
