import mysql.connector
from .models import UsersHasCidadesInDB, UsersHasCidades
from typing import List

MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "redacheck"

async def create_user_has_cidade(user_has_cidades: UsersHasCidades) -> UsersHasCidadesInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        # Obtém os valores de cidade e user_id do objeto user_has_cidades
        cidade = user_has_cidades.cidade
        user_id = user_has_cidades.user_id

        # Prepara e executa a query SQL
        query = ("INSERT INTO users_has_cidades (cidade, users_user_id) VALUES (%s, %s)")
        cursor.execute(query, (cidade, user_id))
        cnx.commit()

        # Retorna um dicionário com os IDs da cidade e do usuário, além dos outros valores do objeto user_has_cidades
        return {"cidade": cidade, "user_id": user_id, **user_has_cidades.dict()}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


async def list_users_has_cidades() -> List[dict]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM users_has_cidades")
        cursor.execute(query)
        cidades_users = cursor.fetchall()
        print(cidades_users)

        cursor.close()
        cnx.close()

        return cidades_users

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

async def get_user_has_cidades(users_has_cidades_id: int) -> UsersHasCidadesInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM users_has_cidades WHERE users_has_cidades_id = %(users_has_cidades_id)s")
        cursor.execute(query, {'users_has_cidades_id': users_has_cidades_id})
        cidade = cursor.fetchone()

        cursor.close()
        cnx.close()

        if cidade:
            return cidade
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def update_user_has_cidades(users_has_cidades_id: int, user_has_cidades: UsersHasCidades) -> dict:
    user_has_cidades_dict = user_has_cidades.dict()
    
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("UPDATE users_has_cidades SET cidade=%(cidade)s, users_user_id=%(user_id)s WHERE users_has_cidades_id=%(users_has_cidades_id)s")
        user_has_cidades_dict["users_has_cidades_id"] = users_has_cidades_id  # Adicionando o ID da cidade ao dicionário
        cursor.execute(query, user_has_cidades_dict)
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Relação atualizada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


async def delete_user_has_cidades(users_has_cidades_id: int) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("DELETE FROM users_has_cidades WHERE users_has_cidades_id = %(users_has_cidades_id)s")
        cursor.execute(query, {'users_has_cidades_id': users_has_cidades_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Turma deleted successfully"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar cidade"}


async def check_user_in_cidade(user_id: str, cidade: str) -> bool:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT COUNT(*) as count FROM users_has_cidades "
                 "WHERE cidade = %(cidade)s AND users_user_id = %(user_id)s")
        cursor.execute(query, {'cidade': cidade, 'user_id': user_id})
        result = cursor.fetchone()
        count = result['count']

        cursor.close()
        cnx.close()

        return count > 0
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
