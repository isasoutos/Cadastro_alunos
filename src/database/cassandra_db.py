from cassandra.cluster import Cluster
from datetime import datetime
import uuid
import time # <-- Adicionamos isso para o sistema saber esperar

# ---------------------------------------------
# CONEXÃO COM RETENTATIVA AUTOMÁTICA (RESILIÊNCIA)
# ---------------------------------------------
print("[SISTEMA] Iniciando conexão com o Cassandra...")
print("[SISTEMA] Como ele foca em alta disponibilidade, pode levar até 1 minuto para inicializar no Docker.")

session = None
max_tentativas = 6

# O Python vai tentar conectar 6 vezes antes de desistir
for tentativa in range(max_tentativas):
    try:
        cluster = Cluster(['cassandra'], port=9042)
        session = cluster.connect()
        print("[SUCESSO] Cassandra conectado!")
        break
    except Exception as e:
        print(f"  -> Cassandra ainda inicializando... (Tentativa {tentativa+1}/{max_tentativas}). Aguardando 10s...")
        time.sleep(10)

# Só cria as tabelas se a conexão deu certo
if session:
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS sistema_auditoria
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
    """)
    session.set_keyspace('sistema_auditoria')

    session.execute("""
        CREATE TABLE IF NOT EXISTS logs_eventos (
            aluno_id UUID,
            evento_id TIMEUUID,
            usuario_id UUID,
            acao TEXT,
            detalhe TEXT,
            data_evento TIMESTAMP,
            PRIMARY KEY (aluno_id, evento_id)
        ) WITH CLUSTERING ORDER BY (evento_id DESC);
    """)

    session.execute("""
        CREATE TABLE IF NOT EXISTS acessos_sensiveis (
            usuario_id UUID,
            acesso_id TIMEUUID,
            endpoint TEXT,
            data_acesso TIMESTAMP,
            PRIMARY KEY (usuario_id, acesso_id)
        ) WITH CLUSTERING ORDER BY (acesso_id DESC);
    """)
    print("[SUCESSO] Tabelas do Cassandra inicializadas e prontas.")
else:
    print("\n[AVISO CRÍTICO] O Cassandra não ligou a tempo. O sistema funcionará, mas os logs de auditoria não serão salvos.\n")

# ---------------------------------------------
# FUNÇÃO: REGISTRAR LOG DE EVENTO
# ---------------------------------------------

def registrar_log_evento(aluno_id, usuario_id, acao, detalhe):
    # Trava de segurança: só tenta gravar se a sessão existir
    if not session:
        return 
        
    query = """
    INSERT INTO logs_eventos (aluno_id, evento_id, usuario_id, acao, detalhe, data_evento)
    VALUES (%s, now(), %s, %s, %s, %s)
    """
    id_aluno_uuid = uuid.UUID(aluno_id) if isinstance(aluno_id, str) else aluno_id
    id_usuario_uuid = uuid.UUID(usuario_id) if isinstance(usuario_id, str) else usuario_id

    session.execute(query, (id_aluno_uuid, id_usuario_uuid, acao, detalhe, datetime.now()))

# ---------------------------------------------
# FUNÇÃO: LISTAR AUDITORIA POR ALUNO
# ---------------------------------------------

def listar_auditoria_por_aluno(aluno_id):
    if not session:
        print("[ERRO] Cassandra está offline.")
        return

    # Tenta converter para UUID, se o usuário digitar errado, o sistema não quebra!
    try:
        id_aluno_uuid = uuid.UUID(aluno_id) if isinstance(aluno_id, str) else aluno_id
    except ValueError:
        print("\n[ERRO DE FORMATO] O Cassandra exige um formato UUID.")
        print(f"Você digitou: '{aluno_id}'. IDs simples como '2' não funcionam aqui.")
        print("Tente usar o UUID de teste: 123e4567-e89b-12d3-a456-426614174000")
        return

    query = "SELECT * FROM logs_eventos WHERE aluno_id = %s"
    resultados = session.execute(query, (id_aluno_uuid,))

    print("\n===== TIMELINE DO ALUNO =====\n")
    encontrou = False
    for row in resultados:
        encontrou = True
        print(f"Data: {row.data_evento}\nUsuário: {row.usuario_id}\nAção: {row.acao}\nDetalhe: {row.detalhe}")
        print("-" * 35)
    
    if not encontrou:
        print("Nenhum log encontrado para este aluno.")

# ---------------------------------------------
# FUNÇÃO: MONITORAR ACESSO
# ---------------------------------------------

def monitorar_acesso(usuario_id, endpoint):
    if not session:
        return

    query = """
    INSERT INTO acessos_sensiveis (usuario_id, acesso_id, endpoint, data_acesso)
    VALUES (%s, now(), %s, %s)
    """
    id_usuario_uuid = uuid.UUID(usuario_id) if isinstance(usuario_id, str) else usuario_id
    session.execute(query, (id_usuario_uuid, endpoint, datetime.now()))

# ---------------------------------------------
# MIDDLEWARE DE LOG AUTOMÁTICO (DECORATOR)
# ---------------------------------------------

def middleware_log(func):
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        registrar_log_evento(
            aluno_id=kwargs.get("aluno_id", "123e4567-e89b-12d3-a456-426614174000"),
            usuario_id=kwargs.get("usuario_id", "987e6543-e21b-12d3-a456-426614174999"),
            acao=func.__name__.upper(),
            detalhe="Função executada com sucesso via middleware"
        )
        return resultado
    return wrapper