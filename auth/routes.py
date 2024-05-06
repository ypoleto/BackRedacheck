from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, status
import jwt
import bcrypt
import mysql.connector
from .models import Token, User
from .database import ALGORITHM, SECRET_KEY, authenticate_user, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES


# Configurações de conexão com o MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "redacheck"

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(request: Request):
    form_data = await request.json()
    username = form_data.get("username")
    password = form_data.get("password")

    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "email": user.email, "nome": user.nome, "tipo": user.tipo, "turmas": user.turmas}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]

# Função para verificar o token
def verify_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/login"))) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Rota protegida que requer o token para acesso
@router.get("/protected/")
async def protected_route(payload: dict = Depends(verify_token)):
    return {"message": "Rota protegida!", "payload": payload}

# Função para autenticar o usuário no MySQL
def authenticate_user(username: str, password: str):
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT user_id, username, email, nome, tipo, password FROM users WHERE username = %(username)s")
        cursor.execute(query, {'username': username})
        user_data = cursor.fetchone()

        cursor.close()
        cnx.close()

        if user_data:
            # Verificar se a senha fornecida corresponde ao hash armazenado no banco de dados
            if bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
                # Se a senha corresponder, retornar os dados do usuário
                return User(**user_data)
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None