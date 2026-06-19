from django.db import models
from django.utils.text import slugify

# Create your models here.


class Assessment(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    pdf = models.FileField(upload_to="assessment/pdf/", null=True, blank=True)
    excel = models.FileField(upload_to="assessment/excel/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class AssessmentResult(models.Model):
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name="results"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="assessment_result/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
