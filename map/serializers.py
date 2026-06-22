from rest_framework import serializers

from .models import Map, MapCategory


class MapCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MapCategory
        fields = [
            "id",
            "name",
            "slug",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class MapSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Map
        fields = [
            "id",
            "name",
            "category",
            "category_name",
            "image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
