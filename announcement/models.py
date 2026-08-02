from django.db import models
from django.utils.text import slugify


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
