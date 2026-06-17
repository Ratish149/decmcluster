from django.db import models


# Create your models here.
class UsefulLink(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    image = models.FileField(upload_to="useful_link_image/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
