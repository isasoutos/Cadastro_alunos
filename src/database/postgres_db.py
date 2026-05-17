import psycopg2

class PostgresModule:
    def __init__(self):
        # Conectando pela rede interna do Docker (container 'postgres')
        self.conexao = psycopg2.connect(
            host="postgres", 
            database="sistema_academico",
            user="postgres",
            password="AH6033"
        )
        self.cursor = self.conexao.cursor()

    def cadastrar_aluno(self, nome, cpf, data_nascimento):
        self.cursor.execute("SELECT cadastrar_aluno(%s::VARCHAR, %s::VARCHAR, %s::DATE)", (nome, cpf, data_nascimento))
        resultado = self.cursor.fetchone()
        self.conexao.commit()
        return resultado[0]

    def cadastrar_professor(self, nome, cpf, especialidade):
        self.cursor.execute("SELECT cadastrar_professor(%s::VARCHAR, %s::VARCHAR, %s::VARCHAR)", (nome, cpf, especialidade))
        resultado = self.cursor.fetchone()
        self.conexao.commit()
        return resultado[0]

    def criar_disciplina(self, nome, codigo):
        self.cursor.execute("SELECT criar_disciplina(%s::VARCHAR, %s::VARCHAR)", (nome, codigo))
        resultado = self.cursor.fetchone()
        self.conexao.commit()
        return resultado[0]

    def vincular_professor_turma(self, professor_id, disciplina_id):
        self.cursor.execute("SELECT vincular_professor_turma(%s::INTEGER, %s::INTEGER)", (professor_id, disciplina_id))
        resultado = self.cursor.fetchone()
        self.conexao.commit()
        return resultado[0]

    def listar_alunos(self):
        self.cursor.execute("SELECT * FROM alunos")
        return self.cursor.fetchall()

    def listar_professores(self):
        self.cursor.execute("SELECT * FROM professores")
        return self.cursor.fetchall()

    def listar_disciplinas(self):
        self.cursor.execute("SELECT * FROM disciplinas")
        return self.cursor.fetchall()