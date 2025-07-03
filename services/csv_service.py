from db import db_connection
from datetime import date, datetime
import csv
import io
import re

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
            formatted_row=[]
            for key in field_order:
                value = row.get(key)
                if key=="data_pagamento":
                    value=value.strftime("%d/%m/%Y")
                formatted_row.append(value)
            writer.writerow(formatted_row)
    # else:
    #     # Se non specificato, usa chiavi del primo record
    #     headers = list(record_set[0].keys())
    #     writer.writerow(headers)
    #     for row in record_set:
    #         writer.writerow([row.get(k, "") for k in headers])

    return output.getvalue()


def validate_row(row, header):
    #Normalizzo e mappo i valodi del csv con gli header
    cleaned_row = []

    for value in row:
        value = value.strip()
        # Simile al preg_match PHP
        if re.match(r"^\d{1,3}(\.\d{3})*(,\d+)?$", value):
            value = value.replace(".", "").replace(",", ".")
        elif re.match(r"^\d+,\d+$", value):
            value = value.replace(",", ".")
        cleaned_row.append(value)
        
    row = dict(zip(header, cleaned_row))
    id_verbale = row["Id Verbale"]
    csv_import = row["Tipo Importo"]

    # Validazione tipo importo
    available_imports = ["Intero", "Frazionato", "Rimborso"]
    if csv_import not in available_imports:
        return False, f"Tipo Importo non valido per il verbale {id_verbale}: '{csv_import}'"

    # Validazione numerica (nessun valore deve essere negativo)
    numerici = [
        "Importo Pagato",
        "Importo Sanzione",
        "Spese di procedura",
        "Spese Postali",
        "Spese Comando",
        "Da Rimborsare"
    ]
    for campo in numerici:
        valore = row.get(campo, "").strip()
        try:
            importo = float(valore) if valore else 0.0
        except ValueError:
            return False, f"Valore non numerico in '{campo}' per il verbale {id_verbale}"
        if importo < 0:
            return False, f"Valore negativo in '{campo}' per il verbale {id_verbale}"
        row[campo] = importo

    # Controllo data pagamento
    data_str = row.get("Data Pagamento", "").strip()
    if not data_str:
        return False, f"Data Pagamento mancante per il verbale {id_verbale}"

    from datetime import datetime
    try:
        data_csv = datetime.strptime(data_str, "%d/%m/%Y").date()
    except ValueError:
        return False, f"Formato data non valido (atteso gg/mm/aaaa) per il verbale {id_verbale}"

    oggi = datetime.today().date()
    if data_csv > oggi:
        return False, f"Data Pagamento futura per il verbale {id_verbale}"

    # # Confronto con data già presente nel DB
    # data_db = db_dates.get(id_verbale)
    # if data_db and data_db != data_csv:
    #     return False, f"La Data Pagamento non corrisponde a quella registrata per il verbale {id_verbale}"

    return row, ""