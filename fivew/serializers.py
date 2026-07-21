from rest_framework import serializers

from .models import FiveWActivity, FiveWImport


class FiveWActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FiveWActivity
        fields = "__all__"


class FiveWImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiveWImport
        fields = "__all__"
        read_only_fields = ("uploaded_by", "verified_by", "created_at", "updated_at")
