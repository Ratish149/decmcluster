from django.db import models
from django.utils.text import slugify

# Create your models here.


class Assessment(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    pdf = models.FileField(upload_to="assessment/pdf/", null=True, blank=True)
    excel = models.FileField(upload_to="assessment/excel/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_public = models.BooleanField(default=False)
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
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AssessmentRegistry(models.Model):
    types_of_survey = models.CharField(max_length=255)
    level_of_survey = models.CharField(max_length=255)
    frequency = models.CharField(max_length=255, null=True, blank=True)
    name_of_survey_tool = models.TextField(null=True, blank=True)
    last_survey_conducted = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.types_of_survey


class AssessmentStats(models.Model):
    name = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
