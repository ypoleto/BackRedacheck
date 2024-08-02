import mysql.connector
from .models import AlunoResponse, GeneroResponse, PropostaResponse, RedacaoInDB, Redacao, RedacaoResponse
from typing import List, Optional

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

        query = ("INSERT INTO redacoes (texto, propostas_proposta_id, users_user_id, titulo, data_envio) "
                 "VALUES (%s, %s, %s, %s, %s)")
        
        # Adapte os valores dos campos e adicione os valores das chaves estrangeiras
        redacao_data = redacao.dict()
        redacao_data['propostas_proposta_id'] = redacao_data.pop('proposta_id')
        redacao_data['users_user_id'] = redacao_data.pop('user_id')

        cursor.execute(query, (redacao_data['texto'], redacao_data['propostas_proposta_id'], redacao_data['users_user_id'], redacao_data['titulo'], redacao_data['data_envio']))
        cnx.commit()

        redacao_id = cursor.lastrowid
        cursor.close()
        cnx.close()

        return RedacaoInDB(**redacao.dict(), id=str(redacao_id))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def list_redacoes(user_id: Optional[int] = None) -> List[RedacaoResponse]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        # Verifica o tipo do usuário
        cursor.execute("SELECT tipo FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise ValueError("User not found")
        
        user_type = user['tipo']
        
        # Define a query com base no tipo do usuário
        if user_type == 'aluno':
            query = """
                SELECT r.redacao_id AS redacao_id, r.texto, r.titulo, r.data_envio, r.propostas_proposta_id AS proposta_id, r.users_user_id AS user_id,
                       p.tema, p.min_palavras, p.max_palavras, p.data_aplicacao, p.data_entrega, p.dificuldade,
                       g.genero_id AS genero_id, g.nome AS genero_nome,
                       u.user_id AS aluno_id, u.nome AS aluno_nome
                FROM redacoes r
                JOIN propostas p ON r.propostas_proposta_id = p.proposta_id
                JOIN generos g ON p.generos_genero_id = g.genero_id
                JOIN users u ON r.users_user_id = u.user_id
                WHERE r.users_user_id = %s;
            """
            cursor.execute(query, (user_id,))
        elif user_type == 'professor':
            query = """
                SELECT r.redacao_id AS redacao_id, r.texto, r.titulo, r.data_envio, r.propostas_proposta_id AS proposta_id, r.users_user_id AS user_id,
                       p.tema, p.min_palavras, p.max_palavras, p.data_aplicacao, p.data_entrega, p.dificuldade,
                       g.genero_id AS genero_id, g.nome AS genero_nome,
                       u.user_id AS aluno_id, u.nome AS aluno_nome
                FROM redacoes r
                JOIN propostas p ON r.propostas_proposta_id = p.proposta_id
                JOIN generos g ON p.generos_genero_id = g.genero_id
                JOIN users u ON r.users_user_id = u.user_id
                WHERE p.users_user_id = %s;
            """
            cursor.execute(query, (user_id,))
        else:
            raise ValueError("Tipo de usuário inválido")
        
        redacoes = cursor.fetchall()

        cursor.close()
        cnx.close()

        return [
            RedacaoResponse(
                id=redacao['redacao_id'],
                texto=redacao['texto'],
                titulo=redacao['titulo'],
                data_envio=redacao['data_envio'],
                proposta=PropostaResponse(
                    id=redacao['proposta_id'],
                    tema=redacao['tema'],
                    min_palavras=redacao['min_palavras'],
                    max_palavras=redacao['max_palavras'],
                    data_aplicacao=redacao['data_aplicacao'],
                    data_entrega=redacao['data_entrega'],
                    dificuldade=redacao['dificuldade'],
                    genero=GeneroResponse(
                        id=redacao['genero_id'],
                        nome=redacao['genero_nome']
                    )
                ),
                aluno=AlunoResponse(
                    id=redacao['aluno_id'],
                    nome=redacao['aluno_nome']
                )
            )
            for redacao in redacoes
        ]
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    except ValueError as err:
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

        query = ("UPDATE redacoes SET texto = %(texto)s, titulo = %(titulo)s, data_envio = %(data_envio)s, propostas_proposta_id = %(proposta_id)s, users_user_id = %(user_id)s WHERE redacao_id = %(redacao_id)s")
        
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
