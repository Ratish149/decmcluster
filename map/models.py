from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


class MapCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Map(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(MapCategory, on_delete=models.CASCADE)
    image = models.FileField(upload_to="map")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
