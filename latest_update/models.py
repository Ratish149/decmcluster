from django.db import models
from django.template.defaultfilters import slugify


class LatestUpdate(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    short_description = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField()
    thumbnail_image = models.FileField(upload_to="latest_update/thumbnail")
    thumbnail_alt_desc = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Thumbnail Alt Description"
    )
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.CharField(max_length=255, null=True, blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_featured", "-created_at"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
