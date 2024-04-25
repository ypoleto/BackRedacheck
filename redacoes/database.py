import mysql.connector
from .models import RedacaoInDB, Redacao
from typing import List
from propostas.database import get_proposta
from turmas.database import get_turma
from users.database import get_user

# Configurações de conexão com o MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "redacheck"

async def create_redacao(redacao: Redacao) -> RedacaoInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("INSERT INTO redacoes (campo1, campo2, campo3) VALUES (%(campo1)s, %(campo2)s, %(campo3)s)")
        cursor.execute(query, redacao.dict())
        cnx.commit()

        redacao_id = cursor.lastrowid
        cursor.close()
        cnx.close()

        return RedacaoInDB(**redacao.dict(), id=str(redacao_id))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def list_redacoes() -> List[dict]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM redacoes")
        cursor.execute(query)
        redacoes = cursor.fetchall()

        cursor.close()
        cnx.close()

        for redacao in redacoes:
            aluno_id = redacao["aluno"]
            aluno = await get_user(aluno_id)
            redacao["aluno"] = aluno  

            proposta_id = redacao["proposta"]
            proposta = await get_proposta(proposta_id)
            redacao["proposta"] = proposta  

        return redacoes

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

async def get_redacao(redacao_id: str) -> RedacaoInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM redacoes WHERE id = %(id)s")
        cursor.execute(query, {'id': redacao_id})
        redacao = cursor.fetchone()

        cursor.close()
        cnx.close()

        if redacao:
            aluno_id = redacao["aluno"]
            aluno = await get_user(aluno_id)
            redacao["aluno"] = aluno  

            proposta_id = redacao["proposta"]
            proposta = await get_proposta(proposta_id)
            redacao["proposta"] = proposta  

            return RedacaoInDB(**redacao)
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def update_redacao(redacao_id: str, redacao: Redacao) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("UPDATE redacoes SET campo1 = %(campo1)s, campo2 = %(campo2)s, campo3 = %(campo3)s WHERE id = %(id)s")
        cursor.execute(query, redacao.dict())
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Redacao atualizada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao atualizar redacao"}

async def delete_redacao(redacao_id: str) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("DELETE FROM redacoes WHERE id = %(id)s")
        cursor.execute(query, {'id': redacao_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Redacao deletada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar redacao"}
