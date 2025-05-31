
from functools import wraps
from fastapi import Request, Response, HTTPException
from utilities.token_handler import gen_token
from services.check_services import validate_user_token
from services.login_services import update_token

def auth_wrapper(func):
    @wraps(func)
    async def wrapper(request: Request, response: Response, *args, **kwargs):
        token=request.cookies.get("token")
        check_user=validate_user_token(token)
        match check_user:
            case 401:
                raise HTTPException(status_code=check_user['status_code'], detail=check_user['detail'])
            case 200:
                if check_user['refresh'] is True:
                    new_token=gen_token()#genero nuovo token, refresh viene generato ma non aggiornato su db
                    result = update_token(new_token['token'], new_token['created_at'], user['id'])

                    #se non true ritorna eccezione e la mostro nei log
                    if result is not True:
                        print(f"errore nel login: {result}")
                        raise HTTPException(status_code=500, detail="Errore durante aggiornamento db")
                        
                    response.set_cookie(key="token", value=new_token['token'])

        return await func(request, response, *args, **kwargs)
    return wrapper