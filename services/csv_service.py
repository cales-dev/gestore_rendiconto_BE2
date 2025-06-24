from db import db_connection
import csv
import io

def generate_export(record_set, field_order=None, field_labels=None):
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")

    if not record_set:
        return ""

    # Determina intestazioni ordinate
    if field_order:
        headers = [field_labels.get(k, k) for k in field_order]
        writer.writerow(headers)
        for row in record_set:
            writer.writerow([row.get(k, "") for k in field_order])
    else:
        # Se non specificato, usa chiavi del primo record
        headers = list(record_set[0].keys())
        writer.writerow(headers)
        for row in record_set:
            writer.writerow([row.get(k, "") for k in headers])

    return output.getvalue()