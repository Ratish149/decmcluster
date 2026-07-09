from django.db import models


# Create your models here.
class DashboardSummary(models.Model):
    estimated_idp = models.IntegerField(default=0)
    evacuation_centres = models.IntegerField(default=0)
    affected_hhs = models.IntegerField(default=0)
    villages_assessed = models.IntegerField(default=0)
    shelter_needs = models.IntegerField(default=0)
    access_to_basic_services = models.IntegerField(default=0)
    children_affected = models.IntegerField(default=0)
    person_with_disabilities = models.IntegerField(default=0)
    active_partners = models.IntegerField(default=0)
    response_coverage = models.IntegerField(default=0)

    def __str__(self):
        return "Dashboard Summary"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Prevent deletion of the singleton instance

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class EvacuationCentreLocationSummary(models.Model):
    province = models.CharField(max_length=100)
    ecs = models.IntegerField(default=0)
    idps = models.IntegerField(default=0)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.province} - {self.ecs}"


class ProvinceSectorSummary(models.Model):
    title = models.CharField(max_length=100)
    percentage = models.FloatField(default=0)

    def __str__(self):
        return f"{self.title} - {self.percentage}%"


class HistoricalEvents(models.Model):
    event = models.CharField(max_length=100)
    year = models.IntegerField()
    impact = models.CharField(max_length=100)

    class Meta:
        ordering = ["year"]

    def __str__(self):
        return f"{self.event} - {self.year}"


class EvacuationCentreList(models.Model):
    province = models.CharField(max_length=100)
    site_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    hhs = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.province} - {self.site_name}"


class ResponseTrackingSummary(models.Model):
    sector = models.CharField(max_length=100)
    partner = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    coverage = models.FloatField(default=0)

    def __str__(self):
        return f"{self.sector} - {self.partner} - {self.status} - {self.coverage}"
