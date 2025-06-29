from typing import Optional
from fastapi import APIRouter, File, Form, HTTPException, Request,Response, UploadFile
from services import report_services, csv_service
from wrapper.auth_wrapper import auth_wrapper
import csv
import io


router = APIRouter()

@router.post("/export/")
@auth_wrapper
async def generate_export_csv(request: Request, response: Response, ente: int=Form()):
    try:
        results = report_services.get_details_data(ente)

        csv_data = csv_service.generate_export(
            results,
            field_order=[
                "id", "stato", "importo_pagato", "data_pagamento", "tipo",
                "importo", "speseprocedura", "spesepostali", "spesecomando", "rimborso"
            ],
            field_labels={
                "id": "Id Verbale",
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
        raise HTTPException(500)
        
@router.post("/upload/")
@auth_wrapper
async def upload_csv(request: Request, response: Response, ente: int=Form(), csv_file: UploadFile=File()):
    expected_filed=[
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
            HTTPException(400, "File vuoto")

        missing = list(set(expected_filed) - set(header))
        if missing:
            raise HTTPException(status_code=400, detail="Missing required columns: " + ", ".join(missing))

        results = []
        for row in read_content:
           #validazione righe
           appo=0

        #TODO metodo per crezione tabella temporanea e inserimento dei dati
        return {"message": "CSV processed successfully", "count": len(results)}
    except Exception as  ex:
        print(ex)
        raise HTTPException(500)