import django_filters

from kobo.models import KoboSubmission


class KoboSubmissionFilter(django_filters.FilterSet):
    asset_uid = django_filters.CharFilter(
        field_name="asset__asset_uid", lookup_expr="exact"
    )
    submitted_after = django_filters.DateTimeFilter(
        field_name="submitted_at", lookup_expr="gte"
    )
    submitted_before = django_filters.DateTimeFilter(
        field_name="submitted_at", lookup_expr="lte"
    )

    class Meta:
        model = KoboSubmission
        fields = ["asset", "asset_uid", "submission_id"]
