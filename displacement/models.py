from django.db import models


# Create your models here.
class Displacement(models.Model):
    OPERATION_STATUS = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )
    operation_code = models.CharField(
        max_length=100, null=True, blank=True, default="0"
    )
    operation = models.CharField(max_length=100)
    admin0_name = models.CharField(max_length=100, null=True, blank=True)
    admin0_pcode = models.CharField(max_length=100, null=True, blank=True)
    admin1_name = models.CharField(max_length=100, null=True, blank=True)
    admin1_pcode = models.CharField(max_length=100, null=True, blank=True)
    admin2_name = models.CharField(max_length=100, null=True, blank=True)
    admin2_pcode = models.CharField(max_length=100, null=True, blank=True)
    admin_level = models.IntegerField(null=True, blank=True)
    num_present_idps = models.IntegerField(null=True, blank=True)
    reporting_date = models.DateField(null=True, blank=True)
    reporting_year = models.IntegerField(null=True, blank=True)
    reporting_month = models.IntegerField(null=True, blank=True)
    round_number = models.IntegerField(null=True, blank=True)
    displacement_reason = models.CharField(max_length=100, null=True, blank=True)
    males_number = models.IntegerField(null=True, blank=True)
    female_number = models.IntegerField(null=True, blank=True)
    males_number_0_4 = models.IntegerField(null=True, blank=True)
    females_number_0_4 = models.IntegerField(null=True, blank=True)
    males_number_5_17 = models.IntegerField(null=True, blank=True)
    females_number_5_17 = models.IntegerField(null=True, blank=True)
    males_number_18_59 = models.IntegerField(null=True, blank=True)
    females_number_18_59 = models.IntegerField(null=True, blank=True)
    males_number_60_plus = models.IntegerField(null=True, blank=True)
    females_number_60_plus = models.IntegerField(null=True, blank=True)
    total_vul_hhs = models.IntegerField(null=True, blank=True)
    idp_origin_admin1_name = models.CharField(max_length=100, null=True, blank=True)
    idp_origin_admin1_pcode = models.CharField(max_length=100, null=True, blank=True)
    assessment_type = models.CharField(max_length=100, null=True, blank=True)
    operation_status = models.CharField(
        max_length=255, choices=OPERATION_STATUS, null=True, blank=True
    )
    idp_destination = models.CharField(max_length=100, null=True, blank=True)
    idp_destination_admin1_name = models.CharField(
        max_length=100, null=True, blank=True
    )
    idp_destination_admin1_pcode = models.CharField(
        max_length=100, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["operation"]),
            models.Index(fields=["admin1_name"]),
            models.Index(fields=["admin2_name"]),
            models.Index(fields=["displacement_reason"]),
            models.Index(fields=["reporting_date"]),
        ]
        verbose_name = "Displacement"
        verbose_name_plural = "Displacement"

    def __str__(self):
        return f"{self.operation} - {self.reporting_date} - {self.reporting_year}"
