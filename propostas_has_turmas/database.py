import mysql.connector
from .models import PropostaHasTurmasInDB, PropostaHasTurmas
from typing import List

MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "redacheck"

async def create_proposta_has_turmas(proposta_has_turmas: PropostaHasTurmas) -> PropostaHasTurmasInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        # Obtém os valores de turma_id e proposta_id do objeto proposta_has_turmas
        turma_id = proposta_has_turmas.turma_id
        proposta_id = proposta_has_turmas.proposta_id

        # Prepara e executa a query SQL
        query = ("INSERT INTO propostas_has_turmas (turmas_turma_id, propostas_proposta_id) VALUES (%s, %s)")
        cursor.execute(query, (turma_id, proposta_id))
        cnx.commit()

        # Retorna um dicionário com os IDs da turma e do usuário, além dos outros valores do objeto proposta_has_turmas
        return {"turma_id": turma_id, "proposta_id": proposta_id, **proposta_has_turmas.dict()}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


async def list_propostas_has_turmas() -> List[dict]:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM propostas_has_turmas")
        cursor.execute(query)
        propostas_turmas = cursor.fetchall()
        print(propostas_turmas)

        cursor.close()
        cnx.close()

        return propostas_turmas

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

async def get_proposta_has_turmas(propostas_has_turmas_id: int) -> PropostaHasTurmasInDB:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT * FROM propostas_has_turmas WHERE propostas_has_turmas_id = %(propostas_has_turmas_id)s")
        cursor.execute(query, {'propostas_has_turmas_id': propostas_has_turmas_id})
        turma = cursor.fetchone()

        cursor.close()
        cnx.close()

        if turma:
            return turma
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

async def update_proposta_has_turmas(propostas_has_turmas_id: int, proposta_has_turmas: PropostaHasTurmas) -> dict:
    proposta_has_turmas_dict = proposta_has_turmas.dict()
    
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("UPDATE propostas_has_turmas SET turmas_turma_id=%(turma_id)s, propostas_proposta_id=%(proposta_id)s WHERE propostas_has_turmas_id=%(propostas_has_turmas_id)s")
        proposta_has_turmas_dict["propostas_has_turmas_id"] = propostas_has_turmas_id  # Adicionando o ID da turma ao dicionário
        cursor.execute(query, proposta_has_turmas_dict)
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Turma atualizada com sucesso"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


async def delete_proposta_has_turmas(propostas_has_turmas_id: int) -> dict:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("DELETE FROM propostas_has_turmas WHERE propostas_has_turmas_id = %(propostas_has_turmas_id)s")
        cursor.execute(query, {'propostas_has_turmas_id': propostas_has_turmas_id})
        cnx.commit()

        cursor.close()
        cnx.close()

        return {"message": "Turma deleted successfully"}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"message": "Erro ao deletar turma"}


async def check_proposta_in_turma(proposta_id: str, turma_id: str) -> bool:
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, port=MYSQL_PORT,
                                      database=MYSQL_DATABASE)
        cursor = cnx.cursor(dictionary=True)

        query = ("SELECT COUNT(*) as count FROM propostas_has_turmas "
                 "WHERE turmas_turma_id = %(turma_id)s AND propostas_proposta_id = %(proposta_id)s")
        cursor.execute(query, {'turma_id': turma_id, 'proposta_id': proposta_id})
        result = cursor.fetchone()
        count = result['count']

        cursor.close()
        cnx.close()

        return count > 0
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
