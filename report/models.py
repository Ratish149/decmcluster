from django.db import models


class Report(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="reports/", null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    date = models.CharField(max_length=255, null=True, blank=True)
    is_situation_report = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
