from django.db import models


# Create your models here.
class ResponseTracking(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="response_tracking/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
