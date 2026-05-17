CREATE KEYSPACE sistema_auditoria
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE sistema_auditoria;

CREATE TABLE logs_eventos (
    aluno_id UUID,
    evento_id TIMEUUID,
    usuario_id UUID,
    acao TEXT,
    detalhe TEXT,
    data_evento TIMESTAMP,
    PRIMARY KEY (aluno_id, evento_id)
) WITH CLUSTERING ORDER BY (evento_id DESC);

CREATE TABLE acessos_sensiveis (
    usuario_id UUID,
    acesso_id TIMEUUID,
    endpoint TEXT,
    data_acesso TIMESTAMP,
    PRIMARY KEY (usuario_id, acesso_id)
) WITH CLUSTERING ORDER BY (acesso_id DESC);
