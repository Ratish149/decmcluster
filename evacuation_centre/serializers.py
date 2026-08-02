from rest_framework import serializers

from .models import EvacuationCentre, EvacuationCentreImport
from .services.import_service import find_duplicate_compound_names


class EvacuationCentreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvacuationCentre
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_compound_name(self, value):
        if not value:
            return value
        clean_name = str(value).strip()
        qs = EvacuationCentre.objects.filter(compound_name__iexact=clean_name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "Duplicate data: An evacuation centre with this compound name already exists."
            )
        return clean_name


class FileImportSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField()

    def validate_file(self, value):
        file_name = value.name.lower()
        if not file_name.endswith((".xlsx", ".xls", ".csv")):
            raise serializers.ValidationError(
                "Only Excel (.xlsx, .xls) or CSV (.csv) files are allowed."
            )

        duplicates = find_duplicate_compound_names(value)
        if duplicates:
            duplicate_str = ", ".join(sorted(duplicates)[:5])
            if len(duplicates) > 5:
                duplicate_str += f" and {len(duplicates) - 5} more"
            raise serializers.ValidationError(
                f"Duplicate data: The uploaded file contains compound name(s) that already exist or appear multiple times: {duplicate_str}."
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


class EvacuationCentreImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvacuationCentreImport
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "verified_by"]
