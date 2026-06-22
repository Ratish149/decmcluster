from rest_framework import serializers

from .models import Assessment, AssessmentRegistry, AssessmentResult


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "pdf",
            "excel",
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


class AssessmentRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentRegistry
        fields = [
            "id",
            "types_of_survey",
            "level_of_survey",
            "frequency",
            "name_of_survey_tool",
            "last_survey_conducted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
