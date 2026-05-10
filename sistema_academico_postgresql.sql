CREATE DATABASE sistema_academico;

CREATE TABLE alunos (
    id_aluno SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE professores (
    id_professor SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    especialidade VARCHAR(100),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE disciplinas (
    id_disciplina SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE professor_turma (
    id_vinculo SERIAL PRIMARY KEY,

    professor_id INTEGER NOT NULL,
    disciplina_id INTEGER NOT NULL,

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_professor
        FOREIGN KEY (professor_id)
        REFERENCES professores(id_professor)
        ON DELETE CASCADE,

    CONSTRAINT fk_disciplina
        FOREIGN KEY (disciplina_id)
        REFERENCES disciplinas(id_disciplina)
        ON DELETE CASCADE
);


CREATE OR REPLACE FUNCTION cadastrar_aluno(
    p_nome VARCHAR,
    p_cpf VARCHAR,
    p_data_nascimento DATE
)
RETURNS TEXT AS
$$
BEGIN

    IF EXISTS (
        SELECT 1
        FROM alunos
        WHERE cpf = p_cpf
    ) THEN
        RETURN 'ERRO: CPF já cadastrado.';
    END IF;

    INSERT INTO alunos(nome, cpf, data_nascimento)
    VALUES (p_nome, p_cpf, p_data_nascimento);

    RETURN 'Aluno cadastrado com sucesso.';

END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION cadastrar_professor(
    p_nome VARCHAR,
    p_cpf VARCHAR,
    p_especialidade VARCHAR
)
RETURNS TEXT AS
$$
BEGIN

    IF EXISTS (
        SELECT 1
        FROM professores
        WHERE cpf = p_cpf
    ) THEN
        RETURN 'ERRO: CPF do professor já cadastrado.';
    END IF;

    INSERT INTO professores(nome, cpf, especialidade)
    VALUES (p_nome, p_cpf, p_especialidade);

    RETURN 'Professor cadastrado com sucesso.';

END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION criar_disciplina(
    p_nome VARCHAR,
    p_codigo VARCHAR
)
RETURNS TEXT AS
$$
BEGIN

    IF EXISTS (
        SELECT 1
        FROM disciplinas
        WHERE codigo = p_codigo
    ) THEN
        RETURN 'ERRO: Código da disciplina já existe.';
    END IF;

    INSERT INTO disciplinas(nome, codigo)
    VALUES (p_nome, p_codigo);

    RETURN 'Disciplina criada com sucesso.';

END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION vincular_professor_turma(
    p_professor_id INTEGER,
    p_disciplina_id INTEGER
)
RETURNS TEXT AS
$$
BEGIN

    IF NOT EXISTS (
        SELECT 1
        FROM professores
        WHERE id_professor = p_professor_id
    ) THEN
        RETURN 'ERRO: Professor não encontrado.';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM disciplinas
        WHERE id_disciplina = p_disciplina_id
    ) THEN
        RETURN 'ERRO: Disciplina não encontrada.';
    END IF;

    INSERT INTO professor_turma(professor_id, disciplina_id)
    VALUES (p_professor_id, p_disciplina_id);

    RETURN 'Professor vinculado à disciplina com sucesso.';

END;
$$ LANGUAGE plpgsql;


INSERT INTO alunos(nome, cpf, data_nascimento)
VALUES ('João Paulo', '12345678901', '2004-10-15');

INSERT INTO professores(nome, cpf, especialidade)
VALUES ('Carlos Silva', '98765432100', 'Ciencia de dados');

INSERT INTO disciplinas(nome, codigo)
VALUES ('Ciencia de dados', 'CDIA01');

INSERT INTO professor_turma(professor_id, disciplina_id)
VALUES (1, 1);


SELECT * FROM alunos;
SELECT * FROM professores;
SELECT * FROM disciplinas;
SELECT * FROM professor_turma;
