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
                "SELECT * FROM tblutenti WHERE username = %s",
                (username,)
            )
            user = cursor.fetchone()
            print(user)
            #Controllo password in chiaro corrisponda con hash su db
            if(check_password(password, user['password'])):
                return user
            
            return None
    finally:
        dbConnection.close()