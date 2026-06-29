from django.db import models


# Create your models here.
class SOP(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="sop", null=True, blank=True)
    is_admin_only = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
