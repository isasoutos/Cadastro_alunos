import os
from neo4j import GraphDatabase

# Se o Docker não achar as variáveis dele, ele vai usar o seu Sandbox como plano B!
URI = os.getenv("NEO4J_URI", "bolt://44.200.239.219:7687") # IP do seu print
USER = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "stuffing-ports-bud") # Sua senha do bloco de notas
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j"
