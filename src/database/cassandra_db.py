from cassandra.cluster import Cluster
from datetime import datetime
import uuid

# ---------------------------------------------
# CONEXÃO E INICIALIZAÇÃO AUTOMÁTICA NO DOCKER
# ---------------------------------------------

# 1. Liga ao contentor do Cassandra usando o nome do serviço definido no Docker
cluster = Cluster(['cassandra'], port=9042)
session = cluster.connect()

# 2. Cria o Keyspace de auditoria caso ele não exista no banco
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS sistema_auditoria
    WITH replication = {
        'class': 'SimpleStrategy',
        'replication_factor': 1
    };
""")

# 3. Define o Keyspace ativo para as próximas operações
session.set_keyspace('sistema_auditoria')

# 4. Cria a tabela de logs de eventos se for a primeira execução
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

# 5. Cria a tabela de acessos sensíveis se for a primeira execução
session.execute("""
    CREATE TABLE IF NOT EXISTS acessos_sensiveis (
        usuario_id UUID,
        acesso_id TIMEUUID,
        endpoint TEXT,
        data_acesso TIMESTAMP,
        PRIMARY KEY (usuario_id, acesso_id)
    ) WITH CLUSTERING ORDER BY (acesso_id DESC);
""")

print("Cassandra conectado e tabelas inicializadas com sucesso.")

# ---------------------------------------------
# FUNÇÃO: REGISTRAR LOG DE EVENTO
# ---------------------------------------------

def registrar_log_evento(aluno_id, usuario_id, acao, detalhe):
    query = """
    INSERT INTO logs_eventos (
        aluno_id,
        evento_id,
        usuario_id,
        acao,
        detalhe,
        data_evento
    )
    VALUES (
        %s,
        now(),
        %s,
        %s,
        %s,
        %s
    )
    """

    # Garante a conversão de strings para objetos UUID caso necessário
    id_aluno_uuid = uuid.UUID(aluno_id) if isinstance(aluno_id, str) else aluno_id
    id_usuario_uuid = uuid.UUID(usuario_id) if isinstance(usuario_id, str) else usuario_id

    session.execute(query, (
        id_aluno_uuid,
        id_usuario_uuid,
        acao,
        detalhe,
        datetime.now()
    ))
    print("Log registrado com sucesso.")

# ---------------------------------------------
# FUNÇÃO: LISTAR AUDITORIA POR ALUNO
# ---------------------------------------------

def listar_auditoria_por_aluno(aluno_id):
    query = """
    SELECT *
    FROM logs_eventos
    WHERE aluno_id = %s
    """
    
    id_aluno_uuid = uuid.UUID(aluno_id) if isinstance(aluno_id, str) else aluno_id
    resultados = session.execute(query, (id_aluno_uuid,))

    print("\n===== TIMELINE DO ALUNO =====\n")
    for row in resultados:
        print(f"Data: {row.data_evento}")
        print(f"Usuário: {row.usuario_id}")
        print(f"Ação: {row.acao}")
        print(f"Detalhe: {row.detalhe}")
        print("-" * 35)

# ---------------------------------------------
# FUNÇÃO: MONITORAR ACESSO
# ---------------------------------------------

def monitorar_acesso(usuario_id, endpoint):
    query = """
    INSERT INTO acessos_sensiveis (
        usuario_id,
        acesso_id,
        endpoint,
        data_acesso
    )
    VALUES (
        %s,
        now(),
        %s,
        %s
    )
    """

    id_usuario_uuid = uuid.UUID(usuario_id) if isinstance(usuario_id, str) else usuario_id

    session.execute(query, (
        id_usuario_uuid,
        endpoint,
        datetime.now()
    ))
    print("Acesso monitorado com sucesso.")

# ---------------------------------------------
# MIDDLEWARE DE LOG AUTOMÁTICO (DECORATOR)
# ---------------------------------------------

def middleware_log(func):
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)

        # Captura os argumentos nomeados para registar no Cassandra automaticamente
        registrar_log_evento(
            aluno_id=kwargs.get("aluno_id"),
            usuario_id=kwargs.get("usuario_id"),
            acao=func.__name__.upper(),
            detalhe="Função executada com sucesso via middleware"
        )
        return resultado
    return wrapper

# ---------------------------------------------
# EXEMPLO DE INTEGRAÇÃO / TESTE
# ---------------------------------------------

@middleware_log
def atualizar_nota(aluno_id, usuario_id, nota):
    print(f"Nota atualizada para {nota} no módulo pedagógico.")

# ---------------------------------------------
# EXECUÇÃO DOS EXEMPLOS DE USO
# ---------------------------------------------

if __name__ == "__main__":
    # Exemplo 1: Registro Direto
    registrar_log_evento(
        aluno_id="123e4567-e89b-12d3-a456-426614174000",
        usuario_id="987e6543-e21b-12d3-a456-426614174999",
        acao="ALTERAR_NOTA",
        detalhe="Professor alterou nota da P1 para 8.5"
    )

    # Exemplo 2: Monitorização de Endpoint
    monitorar_acesso(
        usuario_id="987e6543-e21b-12d3-a456-426614174999",
        endpoint="/admin/alterar-nota"
    )

    # Exemplo 3: Execução Interceptada pelo Middleware Log
    atualizar_nota(
        aluno_id="123e4567-e89b-12d3-a456-426614174000",
        usuario_id="987e6543-e21b-12d3-a456-426614174999",
        nota=9.0
    )

    # Exemplo 4: Consulta à Linha do Tempo
    listar_auditoria_por_aluno("123e4567-e89b-12d3-a456-426614174000")