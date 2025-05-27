from fastapi import APIRouter, Form,HTTPException
from services import login_services

router = APIRouter()

@router.post("/")
def login(username:str = Form(), password:str = Form()):
    try:
        userInfo = login_services.get_user_from_db(username, password)

        if not userInfo:
            raise HTTPException(status_code=401, detail="Credenziali errate")
        
        return {'message':'ok','user':userInfo}
    except Exception as ex:
        print(f"errore nel login: {ex}")
        raise HTTPException(status_code=500, detail="Internal server error")