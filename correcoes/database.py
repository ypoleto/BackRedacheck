import mysql.connector
from .models import CorrecaoInDB, Correcao
from typing import List

# Configurações de conexão com o MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "redacheck"

async def create_correcao(correcao: Correcao) -> CorrecaoInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        # Primeira query para inserir a correção
        query_insert = ("INSERT INTO correcoes (comentarios, redacoes_redacao_id, nota) "
                        "VALUES (%s, %s, %s)")
        
        correcao_data = correcao.dict()
        correcao_data['redacoes_redacao_id'] = correcao_data.pop('redacao_id')

        cursor.execute(query_insert, (correcao_data['comentarios'], correcao_data['redacoes_redacao_id'], correcao_data['nota']))
        cnx.commit()

        # Segunda query para atualizar o status da redação
        query_update = "UPDATE redacoes SET status = 1 WHERE redacao_id = %s"
        cursor.execute(query_update, (correcao_data['redacoes_redacao_id'],))
        cnx.commit()

        correcao_id = cursor.lastrowid
        cursor.close()
        cnx.close()

        return CorrecaoInDB(**correcao.dict(), id=str(correcao_id))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def list_correcoes() -> List[dict]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM correcoes")
        cursor.execute(query)
        correcoes = cursor.fetchall()

        cursor.close()
        cnx.close()

        return correcoes

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

async def get_correcao(correcao_id: str) -> CorrecaoInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT redacoes_redacao_id AS redacao_id, nota, comentarios "
                 "FROM correcoes WHERE correcao_id = %(id)s")
        cursor.execute(query, {'id': correcao_id})
        correcao = cursor.fetchone()

        cursor.close()
        cnx.close()

        if correcao:
            return CorrecaoInDB(**correcao)
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None



async def update_correcao(correcao_id: str, correcao: Correcao) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("UPDATE correcoes SET comentarios = %(comentarios)s, redacoes_redacao_id = %(redacao_id)s, nota = %(nota)s WHERE correcao_id = %(correcao_id)s")
        
        # Convert Correcao object to dictionary
        correcao_data = correcao.dict()
        # Add correcao_id to the dictionary
        correcao_data['correcao_id'] = correcao_id
        
        # Execute the query with the dictionary of parameters
        cursor.execute(query, correcao_data)
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Correcao atualizada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao atualizar correcao"}

async def delete_correcao(correcao_id: str) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("DELETE FROM correcoes WHERE correcao_id = %(id)s")
        cursor.execute(query, {'id': correcao_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Correcao deletada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar correcao"}

async def get_correcao_by_redacao_id(redacao_id: str) -> CorrecaoInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT *, redacoes_redacao_id as redacao_id FROM correcoes WHERE redacoes_redacao_id = %(id)s")
        cursor.execute(query, {'id': redacao_id})
        correcao = cursor.fetchone()

        cursor.close()
        cnx.close()

        if correcao:
            return CorrecaoInDB(**correcao)
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None