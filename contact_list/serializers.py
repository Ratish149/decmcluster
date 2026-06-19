from rest_framework import serializers

from .models import ContactList


class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactList
        fields = [
            "id",
            "name",
            "organization",
            "type",
            "cluster",
            "phone",
            "email",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
