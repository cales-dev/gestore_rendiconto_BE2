from fastapi import APIRouter, File, Form, HTTPException, Request,Response, UploadFile
from services import report_services, csv_service, temptable_service
from wrapper.auth_wrapper import auth_wrapper
import csv
import io
#campi validi nel csv
EXPECTED_FIELD=[
        "Id Pagamento",
        "Id Verbale",
        "Stato Verbale",
        "Importo Pagato",
        "Data Pagamento",
        "Tipo Importo",
        "Importo Sanzione",
        "Spese di procedura",
        "Spese Postali",
        "Spese Comando",
        "Da Rimborsare"
]
    

router = APIRouter()

#Metodo che esporta il csv permettendo all'operatore la modifica dei dati 
@router.post("/export/")
@auth_wrapper
async def generate_export_csv(request: Request, response: Response, ente: int=Form()):
    try:
        results = report_services.get_details_data(ente)
        print(results)
        csv_data = csv_service.generate_export(
            results,
            field_labels={
                "id_pagamento": "Id Pagamento",
                "id_verbale": "Id Verbale",
                "stato": "Stato Verbale",
                "importo_pagato": "Importo Pagato",
                "data_pagamento": "Data Pagamento",
                "tipo": "Tipo Importo",
                "importo": "Importo Sanzione",
                "speseprocedura": "Spese di procedura",
                "spesepostali": "Spese Postali",
                "spesecomando": "Spese Comando",
                "rimborso": "Da Rimborsare"
            }
        )

        response = Response(content=csv_data, media_type="text/csv")
        return response
    except Exception as  ex:
        print(ex)
        raise HTTPException(status_code=500)
        
#Metodo che carica e controlla i dati presi dal csv dell'operatore nella tabella temporanea
@router.post("/upload/")
@auth_wrapper
async def upload_csv(request: Request, response: Response, ente: int=Form(), csv_file: UploadFile=File()):
    try:
        if not ente:
            raise HTTPException(400, detail="Campo ente mancante")
        
        if not csv_file.filename.endswith(".csv"):
            raise HTTPException(400, detail="Caricato file con formato errato")

        file_content=await csv_file.read()
        decoded_file=file_content.decode("utf-8-sig")
        read_content=csv.reader(io.StringIO(decoded_file), delimiter=";")

        header=next(read_content, None)
        if header is None:
            raise HTTPException(400, "File vuoto")
        
        missing = list(set(EXPECTED_FIELD) - set(header))
        if missing:
            raise HTTPException(status_code=400, detail="Intestazioni mancanti: " + ", ".join(missing))

        invalid_header = list(set(header) - set(EXPECTED_FIELD))
        if invalid_header:
            raise HTTPException(status_code=400, detail="Instestazioni non valide: " + ", ".join(invalid_header))
        
        results = []
        for row in read_content:
            #validazione righe
            checked_row, errors=csv_service.validate_row(row, header)
            if errors != "":
                raise HTTPException(status_code=400, detail=f"Il csv non rispetta i controlli in particolare: {errors}")
            
            results.append(checked_row)

        #creo la tabella temporanea e leggo l'errore dal metodo se presente
        create_table_result=temptable_service.create_temp_table_if_not_exists()
        if create_table_result is not True:
            print(create_table_result)
            raise HTTPException(status_code=500, detail=create_table_result)
        
        print(results)
        #inserisco i dati neòla tabella temporanea e leggo l'errore dal metodo se presente
        insert_table_result=temptable_service.insert_into_temp_table(results)
        if insert_table_result is not True:
            print(insert_table_result)
            raise HTTPException(status_code=500, detail=create_table_result)
            
        #TODO metodo per crezione tabella temporanea e inserimento dei dati
        return {"message": "CSV processed successfully", "count": len(results)}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as  ex:
        print(ex)
        raise HTTPException(status_code=500, detail="Internal Server Error")
        