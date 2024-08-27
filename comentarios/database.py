import mysql.connector
from .models import ComentarioInDB, Comentario
from typing import List

# Configurações de conexão com o MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "redacheck"

async def create_comentario(comentario: Comentario) -> ComentarioInDB:
    cnx = None
    cursor = None

    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        # Query para inserir o comentário
        query_insert = ("INSERT INTO comentarios (comentario, paragrafo_id, correcoes_correcao_id) "
                        "VALUES (%s, %s, %s)")
        
        comentario_data = comentario.dict()
        comentario_data['correcoes_correcao_id'] = comentario_data.pop('correcao_id')
        
        cursor.execute(query_insert, (comentario_data['comentario'], comentario_data['paragrafo_id'], comentario_data['correcoes_correcao_id']))
        cnx.commit()

        comentario_id = cursor.lastrowid
        if comentario_id is None:
            raise Exception("Falha ao inserir o comentário no banco de dados. Nenhum ID retornado.")

        return ComentarioInDB(**comentario.dict(), id=comentario_id)
    
    except mysql.connector.Error as err:
        print(f"Erro no MySQL: {err}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

async def list_comentarios() -> List[dict]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM comentarios")
        cursor.execute(query)
        comentarios = cursor.fetchall()

        cursor.close()
        cnx.close()

        return comentarios

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

async def get_comentario(comentario_id: int) -> ComentarioInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM comentarios WHERE comentario_id = %(comentario_id)s")
        cursor.execute(query, {'comentario_id': comentario_id})
        comentario = cursor.fetchone()

        cursor.close()
        cnx.close()

        if comentario:
            comentario['correcao_id'] = comentario.pop('correcoes_correcao_id')
            return ComentarioInDB(**comentario)
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


async def update_comentario(comentario_id: str, comentario: Comentario) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("UPDATE comentarios SET comentarios = %(comentarios)s, redacoes_redacao_id = %(redacao_id)s, nota = %(nota)s WHERE comentario_id = %(comentario_id)s")
        
        # Convert Comentario object to dictionary
        comentario_data = comentario.dict()
        # Add comentario_id to the dictionary
        comentario_data['comentario_id'] = comentario_id
        
        # Execute the query with the dictionary of parameters
        cursor.execute(query, comentario_data)
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Comentario atualizada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao atualizar comentario"}

async def delete_comentario(comentario_id: str) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("DELETE FROM comentarios WHERE comentario_id = %(id)s")
        cursor.execute(query, {'id': comentario_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Comentario deletada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar comentario"}

async def get_comentario_by_redacao_id(redacao_id: str) -> ComentarioInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT *, redacoes_redacao_id as redacao_id FROM comentarios WHERE redacoes_redacao_id = %(id)s")
        cursor.execute(query, {'id': redacao_id})
        comentario = cursor.fetchone()

        cursor.close()
        cnx.close()

        if comentario:
            return ComentarioInDB(**comentario)
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None