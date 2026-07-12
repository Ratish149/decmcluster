from rest_framework import serializers

from .models import EvacutationCentre


class EvacutationCentreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvacutationCentre
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class FileImportSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        file_name = value.name.lower()
        if not file_name.endswith((".xlsx", ".xls", ".csv")):
            raise serializers.ValidationError(
                "Only Excel (.xlsx, .xls) or CSV (.csv) files are allowed."
            )
        return value

