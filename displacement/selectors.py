from django.db.models import Q, Sum

from .models import Displacement


def get_displacement_stats(queryset=None):
    """
    Computes and returns summary analytics for displacement data.
    """
    if queryset is None:
        queryset = Displacement.objects.all()

    stats = queryset.aggregate(
        total_male=Sum("males_number"),
        total_female=Sum("female_number"),
    )

    total_male = stats["total_male"] or 0
    total_female = stats["total_female"] or 0
    total_idp = total_male + total_female

    # Unique operations count
    operation_count = queryset.values("operation").distinct().count()

    # Breakdown by reporting year
    year_stats = (
        queryset
        .exclude(reporting_year__isnull=True)
        .values("reporting_year")
        .annotate(
            total_male=Sum("males_number"),
            total_female=Sum("female_number"),
        )
        .order_by("reporting_year")
    )

    idps_by_year = []
    for item in year_stats:
        y = item["reporting_year"]
        m = item["total_male"] or 0
        f = item["total_female"] or 0
        idps_by_year.append({
            "year": y,
            "total_male": m,
            "total_female": f,
            "total_idp": m + f,
        })

    # Breakdown by admin1_name
    admin1_stats = (
        queryset
        .exclude(Q(admin1_name__isnull=True) | Q(admin1_name=""))
        .values("admin1_name")
        .annotate(
            total_male=Sum("males_number"),
            total_female=Sum("female_number"),
        )
        .order_by("admin1_name")
    )

    admin1_map = {}
    for item in admin1_stats:
        adm = item["admin1_name"]
        if not adm or not adm.strip():
            continue
        adm_name = adm.strip()
        if adm_name not in admin1_map:
            admin1_map[adm_name] = {
                "admin1_name": adm_name,
                "total_male": 0,
                "total_female": 0,
                "total_idp": 0,
            }
        m = item["total_male"] or 0
        f = item["total_female"] or 0
        admin1_map[adm_name]["total_male"] += m
        admin1_map[adm_name]["total_female"] += f
        admin1_map[adm_name]["total_idp"] += m + f

    idps_by_admin1 = list(admin1_map.values())

    return {
        "total_idp": total_idp,
        "total_male": total_male,
        "total_female": total_female,
        "operation_count": operation_count,
        "idps_by_year": idps_by_year,
        "idps_by_admin1": idps_by_admin1,
    }


def get_displacement_unique_filters():
    """
    Returns unique values for admin1_name, operation, and reporting_year.
    """
    admin1_names = (
        Displacement.objects
        .exclude(admin1_name__isnull=True)
        .exclude(admin1_name="")
        .values_list("admin1_name", flat=True)
        .distinct()
        .order_by("admin1_name")
    )
    operations = (
        Displacement.objects
        .exclude(operation__isnull=True)
        .exclude(operation="")
        .values_list("operation", flat=True)
        .distinct()
        .order_by("operation")
    )
    reporting_years = (
        Displacement.objects
        .exclude(reporting_year__isnull=True)
        .values_list("reporting_year", flat=True)
        .distinct()
        .order_by("reporting_year")
    )

    # Strip whitespace from names/operations to ensure uniqueness
    unique_admin1 = sorted(
        list(set(name.strip() for name in admin1_names if name and name.strip()))
    )
    unique_operations = sorted(
        list(set(op.strip() for op in operations if op and op.strip()))
    )
    unique_years = sorted(list(reporting_years))

    return {
        "admin1_names": unique_admin1,
        "operations": unique_operations,
        "reporting_years": unique_years,
    }
