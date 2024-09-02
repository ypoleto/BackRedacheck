import mysql.connector
from .models import TurmaHasUsersInDB, TurmaHasUsersResponse, TurmaHasUsers, UserResponse
from typing import List

MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "redacheck"

async def create_turma_has_user(turma_has_users: TurmaHasUsers) -> TurmaHasUsersInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        # Obtém os valores de turma_id e user_id do objeto turma_has_users
        turma_id = turma_has_users.turma_id
        user_id = turma_has_users.user_id

        # Prepara e executa a query SQL
        query = ("INSERT INTO turmas_has_users (turmas_turma_id, users_user_id) VALUES (%s, %s)")
        cursor.execute(query, (turma_id, user_id))
        cnx.commit()

        # Retorna um dicionário com os IDs da turma e do usuário, além dos outros valores do objeto turma_has_users
        return {"turma_id": turma_id, "user_id": user_id, **turma_has_users.dict()}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


async def list_turmas_has_users(turmaId: int) -> List[dict]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = """
                SELECT
                    t.turma_id, 
                    u.user_id, u.nome AS user_nome, u.username,
                    thu.turmas_has_users_id
                FROM turmas_has_users thu
                JOIN turmas t ON thu.turmas_turma_id = t.turma_id
                JOIN users u ON thu.users_user_id = u.user_id
                WHERE thu.turmas_turma_id = %s
            """
            
        cursor.execute(query, (turmaId,))
        turmasUsers = cursor.fetchall()

        cursor.close()
        cnx.close()
        print(turmasUsers)

        return [
            TurmaHasUsersResponse(
                turma_id=turmaUser['turma_id'],
                turmas_has_users_id=turmaUser['turmas_has_users_id'],
                user=UserResponse(
                    user_id=turmaUser['user_id'],
                    nome=turmaUser['user_nome'],
                    username=turmaUser['username']
                )
            )
            for turmaUser in turmasUsers
        ]
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    except ValueError as err:
        print(f"Error: {err}")
        return []
    
async def get_turma_has_users(turmas_has_users_id: int) -> TurmaHasUsersInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM turmas_has_users WHERE turmas_has_users_id = %(turmas_has_users_id)s")
        cursor.execute(query, {'turmas_has_users_id': turmas_has_users_id})
        turma = cursor.fetchone()

        cursor.close()
        cnx.close()

        if turma:
            return turma
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def update_turma_has_users(turmas_has_users_id: int, turma_has_users: TurmaHasUsers) -> dict:
    turma_has_users_dict = turma_has_users.dict()
    
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("UPDATE turmas_has_users SET turmas_turma_id=%(turma_id)s, users_user_id=%(user_id)s WHERE turmas_has_users_id=%(turmas_has_users_id)s")
        turma_has_users_dict["turmas_has_users_id"] = turmas_has_users_id  # Adicionando o ID da turma ao dicionário
        cursor.execute(query, turma_has_users_dict)
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Turma atualizada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


async def delete_turma_has_users(turmas_has_users_id: int) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("DELETE FROM turmas_has_users WHERE turmas_has_users_id = %(turmas_has_users_id)s")
        cursor.execute(query, {'turmas_has_users_id': turmas_has_users_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Turma deleted successfully"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar turma"}


async def check_user_in_turma(user_id: str, turma_id: str) -> bool:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT COUNT(*) as count FROM turmas_has_users "
                 "WHERE turmas_turma_id = %(turma_id)s AND users_user_id = %(user_id)s")
        cursor.execute(query, {'turma_id': turma_id, 'user_id': user_id})
        result = cursor.fetchone()
        count = result['count']

        cursor.close()
        cnx.close()

        return count > 0
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
