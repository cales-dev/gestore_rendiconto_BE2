from fastapi import APIRouter, HTTPException, Request,Response
from wrapper.auth_wrapper import auth_wrapper

router = APIRouter()

""" Metodo che ritorna le informazioni generali o specifiche di un ente
Implementa auth_wrapper per verificare che l'utente sia loggato per effettuare la chiamata """
@router.get("/summary/")
@auth_wrapper
async def get_summary(request: Request, response: Response):
    return {'ok':True}