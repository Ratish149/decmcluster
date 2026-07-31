from django.template.defaultfilters import slugify
from rest_framework import serializers

from .models import Category, LatestUpdate


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def validate(self, attrs):
        name = attrs.get("name")
        if name and not attrs.get("slug"):
            base_slug = slugify(name)
            slug = base_slug
            count = 1
            qs = Category.objects.all()
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            while qs.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            attrs["slug"] = slug
        return attrs


class LatestUpdateSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source="category", read_only=True)

    class Meta:
        model = LatestUpdate
        fields = [
            "id",
            "category",
            "category_details",
            "title",
            "slug",
            "short_description",
            "description",
            "thumbnail_image",
            "thumbnail_alt_desc",
            "meta_title",
            "meta_description",
            "is_featured",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def validate(self, attrs):
        title = attrs.get("title")
        if title and not attrs.get("slug"):
            base_slug = slugify(title)
            slug = base_slug
            count = 1
            qs = LatestUpdate.objects.all()
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            while qs.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            attrs["slug"] = slug
        return attrs
