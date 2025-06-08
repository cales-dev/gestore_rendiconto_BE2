from db import db_connection

def get_summary_data(ente):
    dbConnection = db_connection.db_connection()
    print(ente)
    try:
        with dbConnection.cursor() as cur:
            if(ente):
                cur.execute("""
                    SELECT 
                    tblverbali.id, 
                    tblcontratti.rifcomune, 
                    tblcontratti.fissoinserito,
                    tblcontratti.fissospedito,
                    tblcontratti.percsanzione,
                    tblcontratti.fissoresponsabile,
                    tblcontratti.rendicontatoperc,
                    SUM(tblpagamenti.importo_pagato) as totale_importo, 
                    COUNT(*) as num_verbali,
                            
                    (SELECT COUNT(*) FROM tblverbali as tblverbali2
                        JOIN tblpagamenti as tblpagamenti2 ON tblpagamenti2.id = tblverbali2.id 
                        WHERE tblpagamenti2.Stato LIKE 'Pagato'
                    ) AS tot_pagati, 
                    (SELECT COUNT(*) FROM tblverbali as tblverbali2
                        JOIN tblpagamenti as tblpagamenti2 ON tblpagamenti2.id = tblverbali2.id 
                        WHERE tblpagamenti2.Stato LIKE 'Da Pagare'
                    ) AS tot_da_pagare, 
                    (SELECT COUNT(*) FROM tblverbali as tblverbali2
                        JOIN tblpagamenti as tblpagamenti2 ON tblpagamenti2.id = tblverbali2.id 
                        WHERE tblpagamenti2.Stato LIKE 'Rimborso') AS tot_rimborso
                            
                    FROM tblverbali
                    JOIN tblcontratti ON tblverbali.id = tblcontratti.id
                    JOIN tblpagamenti ON tblpagamenti.id = tblverbali.id
                    WHERE tblcontratti.rifcomune = %s
                    GROUP BY tblverbali.id, 
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
                    tblverbali.id, 
                    tblcontratti.rifcomune,
                    SUM(tblpagamenti.importo_pagato) as totale_importo, 
                    COUNT(*) as num_verbali
                    FROM tblverbali
                    JOIN tblcontratti ON tblverbali.id = tblcontratti.id
                    JOIN tblpagamenti ON tblpagamenti.id = tblverbali.id
                    GROUP BY tblverbali.id, 
                    tblcontratti.rifcomune
                """)

            results = cur.fetchall()
            return results 
    finally:
        dbConnection.close()
