import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://44.200.239.219:7687")
USER = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "stuffing-ports-bud")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

def executar_query(query, **parametros):
    with GraphDatabase.driver(URI, auth=(USER, PASSWORD)) as driver:
        dados, _, _ = driver.execute_query(query, database_=DATABASE, **parametros)
        return dados

def criar_pre_requisito(cod_origem, cod_destino):
    query = """
    MATCH (d1:Disciplina {codigo: $cod_origem})
    MATCH (d2:Disciplina {codigo: $cod_destino})
    MERGE (d1)-[:EH_REQUISITO_DE]->(d2)
    """
    executar_query(query, cod_origem=cod_origem, cod_destino=cod_destino)

def sugerir_proximas_materias(aluno_id):
    query = """
    MATCH (d:Disciplina)
    WHERE NOT (:Aluno {id: $aluno_id})-[:CONCLUIU]->(d)
    AND ALL(req IN [(r)-[:EH_REQUISITO_DE]->(d) | r] WHERE (:Aluno {id: $aluno_id})-[:CONCLUIU]->(req))
    RETURN d.codigo AS codigo, d.nome AS nome
    """
    resultado = executar_query(query, aluno_id=aluno_id)
    return [{"codigo": registro["codigo"], "nome": registro["nome"]} for registro in resultado]
