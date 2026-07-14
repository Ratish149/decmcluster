from rest_framework import serializers

from .models import Displacement, DisplacementImport


class DisplacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Displacement
        fields = "__all__"
        read_only_fields = ["id"]


class FileImportSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField()

    def validate_file(self, value):
        file_name = value.name.lower()
        if not file_name.endswith((".xlsx", ".xls", ".csv")):
            raise serializers.ValidationError(
                "Only Excel (.xlsx, .xls) or CSV (.csv) files are allowed."
            )
        return value


class DisplacementImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplacementImport
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "verified_by"]

