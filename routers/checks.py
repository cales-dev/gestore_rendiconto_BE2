from fastapi import APIRouter, HTTPException, Request, Response
from utilities.token_handler import check_auth, gen_token
from services.login_services import get_user_with_token, update_token

router = APIRouter()

#Metodo che controlla sessione utente
@router.get("/login/")
def check_user_logged(response:Response, request:Request):
  token=request.cookies.get("token")
  if not token:
    raise HTTPException(status_code=401, detail="User not authorized")
  
  user=get_user_with_token(token)
  if not user:
    raise HTTPException(status_code=401, detail="Invalid token")
  
  user_status=check_auth(user['token_date'])
  if(user_status==False):
    raise HTTPException(status_code=401, detail="Token expired")
  
  if user_status=="refresh":
    new_token=gen_token()#genero nuovo token, refresh viene generato ma non aggiornato su db
    result = update_token(new_token['token'], new_token['created_at'], user['id'])

    #se non true ritorna eccezione e la mostro nei log
    if result is not True:
        print(f"errore nel login: {result}")
        raise HTTPException(status_code=500, detail="Errore durante aggiornamento db")
    
    response.set_cookie(key="token", value=new_token['token'])

  return {'message':'ok','logged':True}