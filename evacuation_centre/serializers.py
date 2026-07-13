from rest_framework import serializers

from .models import EvacuationCentre


class EvacuationCentreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvacuationCentre
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


class EvacuationCentreMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvacuationCentre
        fields = [
            "id",
            "compound_name",
            "latitude",
            "longitude",
            "is_ec_owner_approved",
            "is_ec_govt_approved",
            "province",
        ]
        read_only_fields = fields

