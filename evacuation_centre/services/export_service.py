import csv

from django.http import HttpResponse

from ..models import EvacuationCentre


def generate_evacuation_centre_csv(queryset, requested_columns=None):
    """
    Generates a CSV response containing evacuation centre data.
    Only includes columns specified in requested_columns if they are valid.
    """
    model_fields = [f.name for f in EvacuationCentre._meta.fields]

    # Parse and validate columns
    if requested_columns:
        columns = []
        for col in requested_columns:
            col_cleaned = col.strip().lower()
            if col_cleaned in model_fields:
                columns.append(col_cleaned)
        # Fallback to all fields if no valid columns are requested
        if not columns:
            columns = model_fields
    else:
        columns = model_fields

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="evacuation_centres.csv"'

    writer = csv.writer(response)
    # Write headers
    writer.writerow(columns)

    # Fetch only the fields we need to optimize the database query
    for centre in queryset.only(*columns):
        row = []
        for col in columns:
            val = getattr(centre, col)
            # Format booleans for readability
            if isinstance(val, bool):
                row.append("Yes" if val else "No")
            elif val is None:
                row.append("")
            else:
                row.append(str(val))
        writer.writerow(row)

    return response
