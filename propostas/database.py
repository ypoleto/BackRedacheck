import mysql.connector
from .models import PropostaInDB, Proposta
from typing import List

# Configurações de conexão com o MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "redacheck"

async def create_proposta(proposta: Proposta) -> PropostaInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("INSERT INTO propostas (campo1, campo2, campo3) VALUES (%(campo1)s, %(campo2)s, %(campo3)s)")
        cursor.execute(query, proposta.dict())
        cnx.commit()

        proposta_id = cursor.lastrowid
        cursor.close()
        cnx.close()

        return PropostaInDB(**proposta.dict(), id=str(proposta_id))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def list_propostas(turma: str = None) -> List[dict]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        if turma:
            query = ("SELECT * FROM propostas WHERE turmas LIKE %(turma)s")
            cursor.execute(query, {'turma': f'%{turma}%'})
        else:
            query = ("SELECT * FROM propostas")
            cursor.execute(query)
        
        propostas = cursor.fetchall()

        cursor.close()
        cnx.close()

        return propostas

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

async def get_proposta(proposta_id: str) -> PropostaInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM propostas WHERE id = %(id)s")
        cursor.execute(query, {'id': proposta_id})
        proposta = cursor.fetchone()

        cursor.close()
        cnx.close()

        if proposta:
            return PropostaInDB(**proposta)
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def update_proposta(proposta_id: str, proposta: Proposta) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("UPDATE propostas SET campo1 = %(campo1)s, campo2 = %(campo2)s, campo3 = %(campo3)s WHERE id = %(id)s")
        cursor.execute(query, proposta.dict())
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Proposta atualizada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao atualizar proposta"}

async def delete_proposta(proposta_id: str) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("DELETE FROM propostas WHERE id = %(id)s")
        cursor.execute(query, {'id': proposta_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Proposta deletada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar proposta"}
