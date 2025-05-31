from fastapi import Request, Response, HTTPException
from utilities.token_handler import check_auth
from services.login_services import get_user_with_token
  
def validate_user_token(token):
  if not token:
    return {'status_code':401, 'detail':"User not authorized"}
  
  user=get_user_with_token(token)
  if not user:
    return {'status_code':401, 'detail':"Invalid token"}
  
  user_status=check_auth(user['token_date'])
  if(user_status==False):
    return {'status_code':401, 'detail':"Invalid token"} 
  
  if user_status=="refresh":
    return {'status_code':200,'refresh':True}

  return {'status_code':200, 'message':'ok','logged':True,'user':user}