from rest_framework import serializers

from .models import Assessment, AssessmentResult


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "file",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


class AssessmentResultSerializer(serializers.ModelSerializer):
    assessment_slug = serializers.CharField(source="assessment.slug", read_only=True)

    class Meta:
        model = AssessmentResult
        fields = [
            "id",
            "assessment",
            "assessment_slug",
            "title",
            "description",
            "file",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "assessment", "created_at", "updated_at"]
