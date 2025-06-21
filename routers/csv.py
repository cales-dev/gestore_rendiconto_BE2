from typing import Optional
from fastapi import APIRouter, Form, HTTPException, Request,Response
from services import report_services, csv_service
from wrapper.auth_wrapper import auth_wrapper

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
        