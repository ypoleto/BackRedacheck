import mysql.connector
from .models import TurmaInDB, Turma
from typing import List, Optional

# Configurações de conexão com o MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "redacheck"

async def create_turma(turma: Turma) -> TurmaInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("INSERT INTO turmas (nome, professor, colegio) VALUES (%(nome)s, %(professor)s, %(colegio)s)")
        cursor.execute(query, turma.dict())
        cnx.commit()

        turma_id = cursor.lastrowid
        cursor.close()
        cnx.close()

        return TurmaInDB(**turma.dict(), id=str(turma_id))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None




async def list_turmas(professor_id: Optional[int] = None) -> List[dict]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)
        print(professor_id)
        if professor_id is not None:
            query = ("SELECT * FROM turmas where professor = %s")
            params = (professor_id,) 
        else:
            query = ("SELECT * FROM turmas")
            params = ()
            
        cursor.execute(query, params)
        turmas = cursor.fetchall()

        cursor.close()
        cnx.close()

        return turmas

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

async def get_turma(turma_id: str) -> TurmaInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM turmas WHERE turma_id = %(turma_id)s")
        cursor.execute(query, {'turma_id': turma_id})
        turma = cursor.fetchone()

        cursor.close()
        cnx.close()

        if turma:
            return turma
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def update_turma(turma_id: str, turma: Turma) -> dict:
    turma_dict = turma.dict()

    try:
        cnx = mysql.connector.connect(
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            database=MYSQL_DATABASE
        )
        cursor = cnx.cursor(dictionary=True)

        query = ("UPDATE turmas SET nome=%(nome)s, professor=%(professor)s, colegio=%(colegio)s WHERE turma_id=%(turma_id)s")
        turma_dict["turma_id"] = turma_id
        cursor.execute(query, turma_dict)
        cnx.commit()

        # Recuperar os dados atualizados
        select_query = "SELECT * FROM turmas WHERE turma_id=%s"
        cursor.execute(select_query, (turma_id,))
        updated_turma = cursor.fetchone()

        cursor.close()
        cnx.close()

        if updated_turma:
            return updated_turma
        else:
            return {"message": "Turma não encontrada após atualização"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": f"Erro: {err}"}

async def delete_turma(turma_id: str) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("DELETE FROM turmas WHERE turma_id = %(turma_id)s")
        cursor.execute(query, {'turma_id': turma_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Turma deleted successfully"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar turma"}
