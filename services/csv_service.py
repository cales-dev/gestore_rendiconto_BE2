from datetime import datetime
import pandas as pd
import csv
import io
import re

def generate_export(record_set, field_labels=None):
    dataFrame= pd.DataFrame(record_set)

    #cerco data_pagamento e adatto il formato
    if 'data_pagamento' in dataFrame.columns:
           dataFrame['data_pagamento'] = pd.to_datetime(dataFrame['data_pagamento']).dt.strftime('%d/%m/%Y')

    #uso field_labels per rinominare le intestazioni
    if field_labels:
        dataFrame = dataFrame.rename(columns=field_labels)

    #Ritorno CSV
    buffer = io.StringIO()
    dataFrame.to_csv(buffer, index=False, sep=';')
    return buffer.getvalue()

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