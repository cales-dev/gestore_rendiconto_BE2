from db import db_connection
from datetime import datetime
import csv
import io

#Metodo che genera la tabella temporanea 
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
   
#Metodo che inserisce i dati nella tabella temporanea 
def insert_into_temp_table(results):
    try:
        dbConnection = db_connection.db_connection()
        with dbConnection.cursor() as cursor:
            #Svuoto la tabella ad ogni inserimento
            cursor.execute("TRUNCATE TABLE temp_rendicontazione")

            sql = '''
                    INSERT INTO temp_rendicontazione (
                        id_verbale,
                        id_pagamento,
                        stato_verbale,
                        importo_pagato,
                        data_pagamento,
                        tipo_importo,
                        importo_sanzione,
                        spese_procedura,
                        spese_postali,
                        spese_comando,
                        da_rimborsare
                    ) VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    );
            '''

            for row in results:
                row["Data Pagamento"] = datetime.strptime(row["Data Pagamento"], "%d/%m/%Y").date()
                cursor.execute(
                    sql,(
                        row['Id Verbale'],
                        row['Id Pagamento'],
                        row['Stato Verbale'],
                        row['Importo Pagato'],
                        row['Data Pagamento'],
                        row['Tipo Importo'],
                        row['Importo Sanzione'],
                        row['Spese di procedura'],
                        row['Spese Postali'],
                        row['Spese Comando'],
                        row['Da Rimborsare']
                    )
                )
            
            dbConnection.commit() 
            return True
    except Exception as ex:
        return ex
    finally:
        dbConnection.close()
