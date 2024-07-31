import mysql.connector
from .models import PropostaInDB, Proposta, GeneroResponse, PropostaResponse
from typing import List, Union, Optional
from fastapi import FastAPI, Query

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

        query = ("INSERT INTO propostas (tema, min_palavras, max_palavras, data_aplicacao, data_entrega, dificuldade, generos_genero_id, users_user_id) VALUES (%(tema)s, %(min_palavras)s, %(max_palavras)s, %(data_aplicacao)s, %(data_entrega)s, %(dificuldade)s, %(genero_id)s, %(user_id)s)")
        cursor.execute(query, proposta.dict())
        cnx.commit()

        proposta_id = cursor.lastrowid
        cursor.close()
        cnx.close()

        return PropostaInDB(**proposta.dict(), id=str(proposta_id))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def list_propostas(user_id: Optional[int] = None) -> List[PropostaResponse]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        if user_id is not None:
            query = """
                SELECT p.proposta_id AS id, p.tema, p.min_palavras, p.max_palavras, p.data_aplicacao, p.data_entrega, p.dificuldade,
                       g.genero_id AS genero_id, g.nome AS nome
                FROM propostas p
                JOIN propostas_has_turmas pht ON p.proposta_id = pht.propostas_proposta_id
                JOIN turmas_has_users thu ON pht.turmas_turma_id = thu.turmas_turma_id
                JOIN generos g ON g.genero_id = p.generos_genero_id
                WHERE thu.users_user_id = %s;
            """
            params = (user_id,)
        else:
            query = """
                SELECT p.proposta_id AS id, p.tema, p.min_palavras, p.max_palavras, p.data_aplicacao, p.data_entrega, p.dificuldade,
                       g.genero_id AS genero_id, g.nome AS nome
                FROM propostas p
                JOIN generos g ON g.genero_id = p.generos_genero_id
            """
            params = ()
        
        cursor.execute(query, params)
        
        propostas = cursor.fetchall()

        cursor.close()
        cnx.close()

        return [PropostaResponse(
            id=proposta['id'],
            tema=proposta['tema'],
            min_palavras=proposta['min_palavras'],
            max_palavras=proposta['max_palavras'],
            data_aplicacao=proposta['data_aplicacao'],
            data_entrega=proposta['data_entrega'],
            dificuldade=proposta['dificuldade'],
            genero=GeneroResponse(
                id=proposta['genero_id'],
                nome=proposta['nome']
            )
        ) for proposta in propostas]
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

async def get_proposta(proposta_id: str) -> Union[PropostaInDB, None]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM propostas WHERE proposta_id = %(id)s")
        cursor.execute(query, {'id': proposta_id})
        proposta = cursor.fetchone()

        cursor.close()
        cnx.close()

        if proposta:
            proposta['genero_id'] = proposta.pop('generos_genero_id')
            proposta['user_id'] = proposta.pop('users_user_id')
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

        query = ("UPDATE propostas SET tema = %(tema)s, min_palavras = %(min_palavras)s, max_palavras = %(max_palavras)s, data_aplicacao = %(data_aplicacao)s, data_entrega = %(data_entrega)s, dificuldade = %(dificuldade)s, generos_genero_id = %(genero_id)s, users_user_id = %(user_id)s WHERE proposta_id = %(proposta_id)s")
        proposta_data = proposta.dict()
        proposta_data['proposta_id'] = proposta_id  # Adicionando o proposta_id aos dados da proposta
        cursor.execute(query, proposta_data)
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

        query = ("DELETE FROM propostas WHERE proposta_id = %(id)s")
        cursor.execute(query, {'id': proposta_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Proposta deletada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar proposta"}
