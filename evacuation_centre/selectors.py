from django.db.models import Count, Q, Sum

from .models import EvacuationCentre


def get_evacuation_centre_stats(queryset=None):
    """
    Computes and returns summary analytics for evacuation centres.
    Performs calculations in a single aggregate database query on the provided queryset.
    """
    if queryset is None:
        queryset = EvacuationCentre.objects.all()

    stats = queryset.aggregate(
        total_ec=Count("id"),
        total_internal_capacity=Sum("internal_building_evacuee_capacity"),
        total_water_storage=Sum("water_storage_capacity_litres"),
        # Toilets Sums
        sum_mens_toilet=Sum("total_mens_toilet"),
        sum_womens_toilet=Sum("total_womens_toilet"),
        sum_unisex_toilet=Sum("total_unisex_toilet"),
        sum_disability_access_toilet=Sum("total_disability_access_toilet"),
        # Showers Sums
        sum_mens_shower=Sum("total_mens_shower"),
        sum_womens_shower=Sum("total_womens_shower"),
        sum_unisex_shower=Sum("total_unisex_shower"),
        sum_disability_access_shower=Sum("total_disability_access_shower"),
        # Counts/Sites with features
        water_storage_sites_count=Count(
            "id", filter=Q(water_storage_capacity_litres__gt=0)
        ),
        mens_toilet_sites_count=Count("id", filter=Q(total_mens_toilet__gt=0)),
        womens_toilet_sites_count=Count("id", filter=Q(total_womens_toilet__gt=0)),
        unisex_toilet_sites_count=Count("id", filter=Q(total_unisex_toilet__gt=0)),
        disability_toilet_sites_count=Count(
            "id", filter=Q(total_disability_access_toilet__gt=0)
        ),
        mens_shower_sites_count=Count("id", filter=Q(total_mens_shower__gt=0)),
        womens_shower_sites_count=Count("id", filter=Q(total_womens_shower__gt=0)),
        unisex_shower_sites_count=Count("id", filter=Q(total_unisex_shower__gt=0)),
        disability_shower_sites_count=Count(
            "id", filter=Q(total_disability_access_shower__gt=0)
        ),
        # Boolean Counts
        is_owner_approved_count=Count("id", filter=Q(is_ec_owner_approved=True)),
        is_govt_approved_count=Count("id", filter=Q(is_ec_govt_approved=True)),
        first_aid_kit_available_count=Count(
            "id", filter=Q(first_aid_kit_availability=True)
        ),
        first_aid_trained_person_count=Count(
            "id", filter=Q(first_aid_trained_person=True)
        ),
        kitchen_facilities_count=Count("id", filter=Q(kitchen_cooking_facilities=True)),
        laundry_facilities_count=Count("id", filter=Q(laundry_facilities=True)),
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
            province_map[prov_name] = {"province": prov_name, "total_ec": 0, "count": 0}
        province_map[prov_name]["total_ec"] += item["total_ec"]
        province_map[prov_name]["count"] += item["total_ec"]

    ec_by_province_list = list(province_map.values())

    total_ec = stats["total_ec"] or 0
    owner_approved_pct = (
        round((stats["is_owner_approved_count"] or 0) / total_ec * 100, 2)
        if total_ec
        else 0.0
    )
    govt_approved_pct = (
        round((stats["is_govt_approved_count"] or 0) / total_ec * 100, 2)
        if total_ec
        else 0.0
    )
    first_aid_kit_pct = (
        round((stats["first_aid_kit_available_count"] or 0) / total_ec * 100, 2)
        if total_ec
        else 0.0
    )
    first_aid_trained_pct = (
        round((stats["first_aid_trained_person_count"] or 0) / total_ec * 100, 2)
        if total_ec
        else 0.0
    )
    kitchen_pct = (
        round((stats["kitchen_facilities_count"] or 0) / total_ec * 100, 2)
        if total_ec
        else 0.0
    )
    laundry_pct = (
        round((stats["laundry_facilities_count"] or 0) / total_ec * 100, 2)
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
        "ec_by_province": ec_by_province_list,
        "readiness_indicators": {
            "is_ec_owner_approved": owner_approved_pct,
            "is_ec_govt_approved": govt_approved_pct,
            "first_aid_kit_availability": first_aid_kit_pct,
            "first_aid_trained_person": first_aid_trained_pct,
            "kitchen_cooking_facilities": kitchen_pct,
            "laundry_facilities": laundry_pct,
        },
        "wash_and_facility_indicators": {
            "total_water_storage_capacity": stats["total_water_storage"] or 0,
            "water_storage_sites": stats["water_storage_sites_count"] or 0,
            "mens_toilet": stats["sum_mens_toilet"] or 0,
            "female_toilet": stats["sum_womens_toilet"] or 0,
            "total_unisex_toilet": stats["sum_unisex_toilet"] or 0,
            "total_disability_toilet": stats["sum_disability_access_toilet"] or 0,
            "total_mens_shower": stats["sum_mens_shower"] or 0,
            "total_womens_shower": stats["sum_womens_shower"] or 0,
            "total_unisex_shower": stats["sum_unisex_shower"] or 0,
            "total_disability_shower": stats["sum_disability_access_shower"] or 0,
            "total_disabilityies_shower": stats["sum_disability_access_shower"] or 0,
            "mens_toilet_sites": stats["mens_toilet_sites_count"] or 0,
            "female_toilet_sites": stats["womens_toilet_sites_count"] or 0,
            "total_unisex_toilet_sites": stats["unisex_toilet_sites_count"] or 0,
            "total_disability_toilet_sites": stats["disability_toilet_sites_count"]
            or 0,
            "total_mens_shower_sites": stats["mens_shower_sites_count"] or 0,
            "total_womens_shower_sites": stats["womens_shower_sites_count"] or 0,
            "total_unisex_shower_sites": stats["unisex_shower_sites_count"] or 0,
            "total_disability_shower_sites": stats["disability_shower_sites_count"]
            or 0,
            "kitchen_available_sites": stats["kitchen_facilities_count"] or 0,
            "laundry_available_sites": stats["laundry_facilities_count"] or 0,
        },
    }
