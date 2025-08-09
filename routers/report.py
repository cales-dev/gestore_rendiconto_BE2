from typing import Optional
from fastapi import APIRouter, HTTPException, Request,Response
from wrapper.auth_wrapper import auth_wrapper
from services.report_services import get_summary_data, get_details_data
from services.temptable_service import get_temp_table_data, save_temp_data
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
        summary_data = get_summary_data(ente)
        return {'ok':True, 'result':summary_data}
    except Exception as ex:
        print(f"Errore report/summary/: {ex}")
        raise HTTPException(status_code=500, detail="Errore durante l'estrazione del report")
"""
    Metodo che restituisce il dettaglio di uno specifico ente
"""
@router.get("/details/{ente}")
@auth_wrapper
async def get_details(request:Request, response:Response, ente:int):
    try:
        details_data = get_details_data(ente)
        return {'ok':True, 'result':details_data}
    except Exception as ex:
        print(f"Errore report/details/: {ex}")
        raise HTTPException(status_code=500, detail="Errore durante l'estrazione del dettaglio")
"""
    Metodo richiamato dopo aver caricato il fil csv,
    restituisce le info salvate su temp_rendicontazione
"""
@router.get("/temp/")
@auth_wrapper
async def get_temp_table_info(request:Request, response:Response):
    try:
        temp_data = get_temp_table_data()
        return {'ok':True, 'result':temp_data}
    except Exception as ex:
        print(f"Errore report/details/: {ex}")
        raise HTTPException(status_code=500, detail="Errore durante l'estrazione del dettaglio")
"""
    Metodo che salva le info riportate su temp_rendicontazione
    in tblpagamenti.
"""
@router.post("/save/")
@auth_wrapper
async def save_temp_info(request:Request, response:Response):
    try:
        save_result = save_temp_data()
        return {'ok':save_result}
    except Exception as ex:
        print(f"Errore report/details/: {ex}")
        raise HTTPException(status_code=500, detail="Errore durante l'estrazione del dettaglio")
    