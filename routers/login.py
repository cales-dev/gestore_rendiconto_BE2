from fastapi import APIRouter, Form, HTTPException,Response
from services import login_services
from utilities import token_handler
router = APIRouter()

@router.post("/")
def login(response:Response, username:str = Form(), password:str = Form()):
    try:
        userInfo = login_services.get_user_from_db(username, password)

        if not userInfo:
            raise HTTPException(status_code=401, detail="Credenziali errate")
        
        token_data = token_handler.gen_token()
        print(userInfo)
        result = login_services.update_user_with_token(token_data['token'],
                                               token_data['refresh'],
                                               token_data['created_at'],
                                               token_data['created_at'],#Imposto refresh con stessa data del token
                                               userInfo['id'])
        #se non true ritorna eccezione e la mostro nei log
        if result is not True:
            print(f"errore nel login: {result}")
            raise HTTPException(status_code=500, detail="Errore durante aggiornamento db")
        
        response.set_cookie(
            key="token",
            value=token_data['token'],
            httponly=True,
            secure=False,#localhost
            path="/",
            expires=31557600 #durata di un anno per permettere al refresh di aggiornarlo finchè possibile
        )

        return {'message':'ok','user':userInfo}
    except Exception as ex:
        print(f"errore nel login: {ex}")
        raise HTTPException(status_code=500, detail="Internal server error")