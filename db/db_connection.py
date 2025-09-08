import json
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path

def db_connection(secret_path: str = "db/db_secret.json"):
    # Legge le credenziali dal file JSON
    secret_file = Path(secret_path)

    if not secret_file.exists():
        raise FileNotFoundError(
            f"File di credenziali non trovato: {secret_path}. "
            "Crea un file db_secret.json con i parametri del DB."
        )

    with open(secret_file, "r", encoding="utf-8") as f:
        creds = json.load(f)

    return psycopg2.connect(
        host=creds["host"],
        port=creds.get("port", 5432),
        database=creds["database"],
        user=creds["user"],
        password=creds["password"],
        cursor_factory=RealDictCursor
    )