import mysql.connector
from .models import RedacaoInDB, Redacao
from typing import List

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

        query = ("INSERT INTO redacoes (texto, propostas_proposta_id, users_user_id) "
                 "VALUES (%s, %s, %s)")
        
        # Adapte os valores dos campos e adicione os valores das chaves estrangeiras
        redacao_data = redacao.dict()
        redacao_data['propostas_proposta_id'] = redacao_data.pop('proposta_id')
        redacao_data['users_user_id'] = redacao_data.pop('user_id')

        cursor.execute(query, (redacao_data['texto'], redacao_data['propostas_proposta_id'], redacao_data['users_user_id']))
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

        query = ("SELECT propostas_proposta_id AS proposta_id, users_user_id AS user_id, texto "
                 "FROM redacoes WHERE redacao_id = %(id)s")
        cursor.execute(query, {'id': redacao_id})
        redacao = cursor.fetchone()

        cursor.close()
        cnx.close()

        if redacao:
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

        query = ("UPDATE redacoes SET texto = %(texto)s, propostas_proposta_id = %(proposta_id)s, users_user_id = %(user_id)s WHERE redacao_id = %(redacao_id)s")
        
        # Convert Redacao object to dictionary
        redacao_data = redacao.dict()
        # Add redacao_id to the dictionary
        redacao_data['redacao_id'] = redacao_id
        
        # Execute the query with the dictionary of parameters
        cursor.execute(query, redacao_data)
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

        query = ("DELETE FROM redacoes WHERE redacao_id = %(id)s")
        cursor.execute(query, {'id': redacao_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Redacao deletada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar redacao"}
