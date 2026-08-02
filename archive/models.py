from django.db import models


class Archive(models.Model):
    survey_type = models.CharField(max_length=100)
    date = models.DateField()
    survery_tools = models.TextField(null=True, blank=True)
    level = models.CharField(max_length=255)
    file = models.FileField(upload_to="archive/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Archive"
        verbose_name_plural = "Archives"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["survey_type"]),
            models.Index(fields=["level"]),
        ]

    def __str__(self):
        return self.survey_type
