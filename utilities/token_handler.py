import secrets
import pytz
from datetime import timedelta, datetime

#Date di scandenza dei toke, rispettivamente 1 ora e 2 settimane
TOKEN_EXPIRE = timedelta(minutes=60)
REFRESH_EXPIRE = timedelta(weeks=2)

#Genera token da salvare su db
def gen_token():
    token_start_date = datetime.now(pytz.utc)

    token_data={
        "token":secrets.token_urlsafe(32),
        "refresh":secrets.token_urlsafe(32),
        "created_at":token_start_date
    }

    return token_data

#Controlli sulle scadenze dei token
def check_token_expiration(token_date):
    return datetime.now(pytz.utc) - token_date < TOKEN_EXPIRE

def check_refresh_expiration(token_date):
    return datetime.now(pytz.utc) - token_date < REFRESH_EXPIRE