from django.db.models import Count, Q, Sum

from .models import EvacutationCentre


def get_evacuation_centre_stats(queryset=None):
    """
    Computes and returns summary analytics for evacuation centres.
    Performs calculations in a single aggregate database query on the provided queryset.
    """
    if queryset is None:
        queryset = EvacutationCentre.objects.all()

    stats = queryset.aggregate(
        total_ec=Count("id"),
        total_internal_capacity=Sum("internal_building_evacuee_capacity"),
        total_water_storage=Sum("water_storage_capacity_litres"),
        # Toilets
        sum_mens_toilet=Sum("total_mens_toilet"),
        sum_womens_toilet=Sum("total_womens_toilet"),
        sum_unisex_toilet=Sum("total_unisex_toilet"),
        sum_disability_access_toilet=Sum("total_disability_access_toilet"),
        # Showers
        sum_mens_shower=Sum("total_mens_shower"),
        sum_womens_shower=Sum("total_womens_shower"),
        sum_unisex_shower=Sum("total_unisex_shower"),
        sum_disability_access_shower=Sum("total_disability_access_shower"),
        # Conditional Boolean counts
        is_govt_approved_count=Count("id", filter=Q(is_ec_govt_approved=True)),
        first_aid_kit_available_count=Count(
            "id", filter=Q(first_aid_kit_availability=True)
        ),
        first_aid_trained_person_count=Count(
            "id", filter=Q(first_aid_trained_person=True)
        ),
        kitchen_facilities_count=Count("id", filter=Q(kitchen_cooking_facilities=True)),
        laundry_facilities_count=Count("id", filter=Q(laundry_facilities=True)),
        has_toilets_count=Count(
            "id",
            filter=(
                Q(total_mens_toilet__gt=0)
                | Q(total_womens_toilet__gt=0)
                | Q(total_unisex_toilet__gt=0)
                | Q(total_disability_access_toilet__gt=0)
            ),
        ),
        has_showers_count=Count(
            "id",
            filter=(
                Q(total_mens_shower__gt=0)
                | Q(total_womens_shower__gt=0)
                | Q(total_unisex_shower__gt=0)
                | Q(total_disability_access_shower__gt=0)
            ),
        ),
    )

    total_toilets = (
        (stats["sum_mens_toilet"] or 0)
        + (stats["sum_womens_toilet"] or 0)
        + (stats["sum_unisex_toilet"] or 0)
        + (stats["sum_disability_access_toilet"] or 0)
    )

    total_showers = (
        (stats["sum_mens_shower"] or 0)
        + (stats["sum_womens_shower"] or 0)
        + (stats["sum_unisex_shower"] or 0)
        + (stats["sum_disability_access_shower"] or 0)
    )

    province_stats = (
        queryset
        .exclude(Q(province__isnull=True) | Q(province=""))
        .values("province")
        .annotate(
            total_ec=Count("id"),
            idp=Count("id", filter=Q(is_ec_owner_approved=True)),
        )
        .order_by("province")
    )

    province_map = {}
    for item in province_stats:
        prov = item["province"]
        if not prov or not prov.strip():
            continue
        prov_name = prov.strip()
        if prov_name not in province_map:
            province_map[prov_name] = {"province": prov_name, "total_ec": 0, "idp": 0}
        province_map[prov_name]["total_ec"] += item["total_ec"]
        province_map[prov_name]["idp"] += item["idp"]

    evacutation_center_list = list(province_map.values())

    total_ec = stats["total_ec"] or 0
    toilets_pct = (
        round(((stats["has_toilets_count"] or 0) / total_ec) * 100, 2)
        if total_ec
        else 0.0
    )
    showers_pct = (
        round(((stats["has_showers_count"] or 0) / total_ec) * 100, 2)
        if total_ec
        else 0.0
    )
    kitchen_pct = (
        round(((stats["kitchen_facilities_count"] or 0) / total_ec) * 100, 2)
        if total_ec
        else 0.0
    )
    laundry_pct = (
        round(((stats["laundry_facilities_count"] or 0) / total_ec) * 100, 2)
        if total_ec
        else 0.0
    )

    return {
        "total_ec": total_ec,
        "total_internal_capacity": stats["total_internal_capacity"] or 0,
        "total_toilets": total_toilets,
        "total_water_storage": stats["total_water_storage"] or 0,
        "total_showers": total_showers,
        "is_govt_approved": stats["is_govt_approved_count"] or 0,
        "first_aid_kit_available": stats["first_aid_kit_available_count"] or 0,
        "first_aid_trained_person": stats["first_aid_trained_person_count"] or 0,
        "wash_and_facilities": {
            "toilets": toilets_pct,
            "showers": showers_pct,
            "kitchen_facilities": kitchen_pct,
            "laundry_facilities": laundry_pct,
        },
        "evacutation_center": evacutation_center_list,
    }
