from django.db import models


# Create your models here.
class ContactList(models.Model):
    TYPE_CHOICES = (
        ("National Co-lead", "National Co-lead"),
        ("Sub-National", "Sub-National"),
        ("Inter-Cluster", "Inter-Cluster"),
    )
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, default="", db_index=True)
    cluster = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255)
    order = models.IntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
