import mysql.connector
from .models import GeneroInDB, Genero
from typing import List

# Configurações de conexão com o MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "redacheck"

async def create_genero(genero: Genero) -> GeneroInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("INSERT INTO generos (nome) VALUES (%(nome)s)")
        cursor.execute(query, genero.dict())
        cnx.commit()

        genero_id = cursor.lastrowid
        cursor.close()
        cnx.close()

        return GeneroInDB(**genero.dict(), id=str(genero_id))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def list_generos() -> List[dict]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM generos")
        cursor.execute(query)
        generos = cursor.fetchall()

        cursor.close()
        cnx.close()

        return generos

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

async def get_genero(genero_id: str) -> GeneroInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM generos WHERE genero_id = %(genero_id)s")
        cursor.execute(query, {'genero_id': genero_id})
        genero = cursor.fetchone()

        cursor.close()
        cnx.close()

        if genero:
            return GeneroInDB(**genero)
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def update_genero(genero_id: str, genero: Genero) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("UPDATE generos SET nome = %s WHERE genero_id = %s")
        cursor.execute(query, (genero.nome, genero_id))
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Genero atualizado com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao atualizar genero"}

async def delete_genero(genero_id: str) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("DELETE FROM generos WHERE genero_id = %(genero_id)s")
        cursor.execute(query, {'genero_id': genero_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Genero deletado com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar genero"}
