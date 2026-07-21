from rest_framework import serializers

from .models import VillageAssessment, VillageAssessmentImport


class VillageAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VillageAssessment
        fields = "__all__"


class VillageAssessmentImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = VillageAssessmentImport
        fields = "__all__"
        read_only_fields = ("uploaded_by", "verified_by", "created_at", "updated_at")
