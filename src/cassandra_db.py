from cassandra.cluster import Cluster
from datetime import datetime

# ---------------------------------------------
# CONEXÃO COM O CASSANDRA
# ---------------------------------------------

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('sistema_auditoria')

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

    session.execute(query, (
        aluno_id,
        usuario_id,
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

    resultados = session.execute(query, (aluno_id,))

    print("\n===== TIMELINE DO ALUNO =====\n")

    for row in resultados:
        print(f"""
Data: {row.data_evento}
Usuário: {row.usuario_id}
Ação: {row.acao}
Detalhe: {row.detalhe}
-----------------------------------
""")

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

    session.execute(query, (
        usuario_id,
        endpoint,
        datetime.now()
    ))

    print("Acesso monitorado com sucesso.")

# ---------------------------------------------
# MIDDLEWARE DE LOG AUTOMÁTICO
# ---------------------------------------------

def middleware_log(func):

    def wrapper(*args, **kwargs):

        resultado = func(*args, **kwargs)

        registrar_log_evento(
            aluno_id=kwargs.get("aluno_id"),
            usuario_id=kwargs.get("usuario_id"),
            acao=func.__name__,
            detalhe="Função executada com sucesso"
        )

        return resultado

    return wrapper

# ---------------------------------------------
# EXEMPLO DE INTEGRAÇÃO
# ---------------------------------------------

@middleware_log
def atualizar_nota(aluno_id, usuario_id, nota):

    print(f"Nota atualizada para {nota}")

# ---------------------------------------------
# EXEMPLOS DE USO
# ---------------------------------------------

registrar_log_evento(
    aluno_id="123e4567-e89b-12d3-a456-426614174000",
    usuario_id="987e6543-e21b-12d3-a456-426614174999",
    acao="ALTERAR_NOTA",
    detalhe="Professor alterou nota da P1 para 8.5"
)

listar_auditoria_por_aluno(
    "123e4567-e89b-12d3-a456-426614174000"
)

monitorar_acesso(
    usuario_id="987e6543-e21b-12d3-a456-426614174999",
    endpoint="/admin/alterar-nota"
)

atualizar_nota(
    aluno_id="123e4567-e89b-12d3-a456-426614174000",
    usuario_id="987e6543-e21b-12d3-a456-426614174999",
    nota=9.0
)
