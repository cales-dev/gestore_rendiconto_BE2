import bcrypt

#Metodo che genera la password per gli utenti
def convert_hash_password(pwd:str):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(pwd.encode('utf-8'), salt)
    return hash.decode('utf-8')

#Metodo che crea l'hash della password e lo confronta con l'hash nel db  
def check_password(pwd:str, hash:str):
    return bcrypt.checkpw(pwd.encode('utf-8'), hash.encode('utf-8'))


