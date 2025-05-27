import psycopg2
from db import db_connection
from utilities.security import check_password

#Metodo che cerca utente nel db e verifica password
def get_user_from_db(username, password):
    dbConnection = db_connection.db_connection()
    try:
        #seleziono utente
        with dbConnection.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, password FROM tblutenti WHERE username = %s",
                (username,)
            )
            user = cursor.fetchone()
            #Controllo password in chiaro corrisponda con hash su db
            if(check_password(password, user['password'])):
                userInfo={"id":user['id'],"username":user['username']} #passo solo info non sensibili
                return userInfo
            
            return None
    finally:
        dbConnection.close()


def update_user_with_token(token, refresh, creation_date, id):
    dbConnection = db_connection.db_connection()
    try:
        with dbConnection.cursor() as cursor:
            cursor.execute(
                "UPDATE tblutenti SET token=%s, refresh=%s, token_date=%s WHERE id = %s",
                (token, refresh, creation_date, id)
            )
            dbConnection.commit()
        return True
    except Exception as ex:
        return ex 
    finally:
        dbConnection.close()