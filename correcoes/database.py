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

        query = ("INSERT INTO correcoes (campo1, campo2, campo3) VALUES (%(campo1)s, %(campo2)s, %(campo3)s)")
        cursor.execute(query, correcao.dict())
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

        query = ("SELECT * FROM correcoes WHERE id = %(id)s")
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

        query = ("UPDATE correcoes SET campo1 = %(campo1)s, campo2 = %(campo2)s, campo3 = %(campo3)s WHERE id = %(id)s")
        cursor.execute(query, correcao.dict())
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

        query = ("DELETE FROM correcoes WHERE id = %(id)s")
        cursor.execute(query, {'id': correcao_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Correcao deletada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar correcao"}
