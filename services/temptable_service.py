from db import db_connection
import csv
import io


def create_temp_table_if_not_exists():
    try:
        
        dbConnection = db_connection.db_connection()
        #seleziono utente
        with dbConnection.cursor() as cursor:
            sql = '''
                    CREATE TABLE IF NOT EXISTS temp_rendicontazione (
                    ID BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    id_verbale BIGINT NOT NULL,
                    id_pagamento BIGINT NOT NULL,
                    stato_verbale VARCHAR(255),
                    importo_pagato DECIMAL(10,2),
                    data_pagamento DATE,
                    tipo_importo VARCHAR(20) CHECK (tipo_importo IN ('Intero', 'Frazionato', 'Rimborso')) NOT NULL,
                    importo_sanzione DECIMAL(10,2),
                    spese_procedura DECIMAL(10,2),
                    spese_postali DECIMAL(10,2),
                    spese_comando DECIMAL(10,2),
                    da_rimborsare DECIMAL(10,2)
                );
            '''
            cursor.execute(sql)
            dbConnection.commit() 
            return True
    except Exception as ex:
            return ex
    finally:
        dbConnection.close()
   
def insert_into_temp_table():
    try:
        dbConnection = db_connection.db_connection()
        with dbConnection.cursor() as cursor:

            return True
    except Exception as ex:
        return ex
    finally:
        dbConnection.close()
