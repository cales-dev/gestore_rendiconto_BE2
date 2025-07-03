from db import db_connection

def get_summary_data(ente):
    dbConnection = db_connection.db_connection()
    try:
        with dbConnection.cursor() as cur:
            if(ente):
                cur.execute("""
                    SELECT 
                    tblverbali.id, 
                    tblverbali.id_ente as ente_id,  
                    tblcontratti.rifcomune, 
                    tblcontratti.fissoinserito,
                    tblcontratti.fissospedito,
                    tblcontratti.percsanzione,
                    tblcontratti.fissoresponsabile,
                    tblcontratti.rendicontatoperc,
                    SUM(tblpagamenti.importo_pagato) as totale_importo, 
                    COUNT(*) as num_verbali,
                            
                    (SELECT COUNT(*) 
                        FROM tblverbali as tblverbali2
                        JOIN tblcontratti as tblcontratti2 ON tblverbali2.id_ente = tblcontratti2.id
                        JOIN tblpagamenti as tblpagamenti2 ON tblpagamenti2.id = tblverbali2.id 
                        WHERE tblpagamenti2.Stato = 'Pagato'
                        AND tblcontratti2.rifcomune = tblcontratti.rifcomune
                    ) AS tot_pagati, 
                    (SELECT COUNT(*) FROM tblverbali as tblverbali2
                        JOIN tblcontratti as tblcontratti2 ON tblverbali2.id_ente = tblcontratti2.id
                        JOIN tblpagamenti as tblpagamenti2 ON tblpagamenti2.id = tblverbali2.id 
                        WHERE tblpagamenti2.Stato = 'Da Pagare'
                        AND tblcontratti2.rifcomune = tblcontratti.rifcomune
                    ) AS tot_da_pagare, 
                    (SELECT COUNT(*) FROM tblverbali as tblverbali2
                        JOIN tblcontratti as tblcontratti2 ON tblverbali2.id_ente = tblcontratti2.id
                        JOIN tblpagamenti as tblpagamenti2 ON tblpagamenti2.id = tblverbali2.id 
                        WHERE tblpagamenti2.Stato = 'Rimborso'
                        AND tblcontratti2.rifcomune = tblcontratti.rifcomune
                    )  AS tot_rimborso
                            
                    FROM tblverbali
                    JOIN tblcontratti ON tblverbali.id_ente = tblcontratti.id
                    JOIN tblpagamenti ON tblpagamenti.id_verbale = tblverbali.id
                    WHERE tblcontratti.rifcomune = %s
                    GROUP BY tblverbali.id_ente, 
                    tblverbali.id, 
                    tblcontratti.rifcomune, 
                    tblcontratti.fissoinserito,
                    tblcontratti.fissospedito,
                    tblcontratti.percsanzione,
                    tblcontratti.fissoresponsabile,
                    tblcontratti.rendicontatoperc
                """, 
                (ente,))
            else:
                cur.execute("""
                    SELECT 
                        tblverbali.id_ente as ente_id, 
                        tblcontratti.rifcomune,
                        SUM(tblpagamenti.importo_pagato) AS totale_importo, 
                        COUNT(tblverbali.id) AS num_verbali
                    FROM tblverbali
                    JOIN tblcontratti ON tblverbali.id_ente = tblcontratti.id  
                    JOIN tblpagamenti ON tblpagamenti.id_verbale = tblverbali.id
                    GROUP BY 
                        tblverbali.id_ente,
                        tblcontratti.rifcomune
                """)

            results = cur.fetchall()
            return results 
    finally:
        dbConnection.close()

def get_details_data(ente):
    dbConnection = db_connection.db_connection()
    try:
        with dbConnection.cursor() as cur:
            cur.execute("""
                SELECT 
                tblpagamenti.id as id_pagamento, 
                tblverbali.id as id_verbale,
                stato,
                importo_pagato,
                data_pagamento,
                tipo,
                importo,
                speseprocedura,
                spesepostali,
                spesecomando,
                rimborso
                FROM tblpagamenti
                JOIN tblverbali ON tblpagamenti.id_verbale = tblverbali.id
                JOIN tblspese ON tblspese.id_verbale = tblverbali.id
                WHERE tblverbali.id_ente = %s
                ORDER BY tblverbali.id ASC
            """, 
            (ente,))

            results = cur.fetchall()
            return results 
    finally:
        dbConnection.close()