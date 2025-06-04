from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Request,Response
from wrapper.auth_wrapper import auth_wrapper
from services.report_services import get_summary_data
router = APIRouter()

""" 
    Metodo che ritorna le informazioni generali o specifiche di un ente
    Implementa auth_wrapper (decorator custom)
    per verificare che l'utente sia loggato per effettuare la chiamata 
"""
@router.get("/summary/")
@router.get("/summary/{ente}")
@auth_wrapper
async def get_summary(request: Request, response: Response, ente: Optional[str] = None):
    try: 
        print(ente)
        summary_data = get_summary_data(ente)
        return {'ok':True, 'result':summary_data}
    except Exception as ex:
        print(f"Errore report/summary/: {ex}")
        raise HTTPException(status_code=500, detail="Errore durante l'estrazione del report")