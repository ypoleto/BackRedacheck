import mysql.connector
from .models import UserInDB, User
from passlib.context import CryptContext
from turmas.database import get_turma
from typing import List

# Configurações de conexão com o MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "redacheck"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

  
async def create_user(user: User) -> UserInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        new_user_data = user.model_dump()
        new_user_data["password"] = get_password_hash(new_user_data["password"])

        # Inserir usuário na tabela de usuários
        user_query = ("INSERT INTO users (username, email, password, nome, tipo) VALUES "
                      "(%(username)s, %(email)s, %(password)s, %(nome)s, %(tipo)s)")
        cursor.execute(user_query, new_user_data)
        cnx.commit()

        # Obter o ID do usuário recém-inserido
        user_id = cursor.lastrowid

        # Processar cidades e turmas separadas por vírgula
       # Convertendo IDs das cidades em inteiros
        cidades = []
        if new_user_data["cidades"]:
            cidades = [int(city_id) for city_id in new_user_data["cidades"].split(",")]

        # Convertendo IDs das turmas em inteiros
        turmas = []
        if new_user_data["turmas"]:
            turmas = [int(turma_id) for turma_id in new_user_data["turmas"].split(",")]

        # Inserir relações nas tabelas users_has_cidades e turmas_has_users usando executemany
        cidades_values = [(city_id, user_id) for city_id in cidades]  # Adaptado para {cidade, users_user_id}
        cidades_query = ("INSERT INTO users_has_cidades (cidade4[], users_user_id) VALUES "
                         "(%s, %s)")
        cursor.executemany(cidades_query, cidades_values)

        turmas_values = [(user_id, turma_id) for turma_id in turmas]  # Adaptado para {users_user_id, turmas_turma_id}
        turmas_query = ("INSERT INTO turmas_has_users (users_user_id, turmas_turma_id) VALUES "
                        "(%s, %s)")
        cursor.executemany(turmas_query, turmas_values)

        cnx.commit()
        cursor.close()
        cnx.close()

        return UserInDB(**new_user_data, id=str(user_id))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None




async def list_users() -> List[dict]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM users")
        cursor.execute(query)
        users = cursor.fetchall()

        cursor.close()
        cnx.close()

        return users

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

async def get_user(user_id: str) -> UserInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM users WHERE id = %(id)s")
        cursor.execute(query, {'id': user_id})
        user = cursor.fetchone()

        cursor.close()
        cnx.close()

        if user:
            user_id = user["id"]
            user.pop("id", None)
            user["turma"] = await get_turma(user["turma_id"])
            return UserInDB(**user, id=user_id)
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def update_user(user_id: str, user: User) -> dict:
    user_dict = user.dict()
    
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)
        query = ("UPDATE users SET nome=%(nome)s, username=%(username)s, tipo=%(tipo)s WHERE user_id=%(user_id)s")
        user_dict["user_id"] = user_id  # Adicionando o ID da user ao dicionário
        cursor.execute(query, user_dict)
        cnx.commit()
        cursor.close()
        cnx.close()
        return {"message": "User atualizado com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def update_user_password(user_id: str, new_password: str) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)
        
        hashed_password = get_password_hash(new_password)
        
        query = ("UPDATE users SET password=%s WHERE id=%s")
        
        cursor.execute(query, (hashed_password, user_id))
        
        cnx.commit()
        cursor.close()
        cnx.close()
        
        return {"message": "Senha do usuário atualizada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao atualizar a senha do usuário"}

async def delete_user(user_id: str) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("DELETE FROM users WHERE user_id = %(id)s")
        cursor.execute(query, {'id': user_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "User deleted successfully"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar usuário"}
