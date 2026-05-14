import 0

# =========================================
# CONEXÃO COM O BANCO DE DADOS
# =========================================

conexao = psycopg2.connect(
    host="localhost",
    database="sistema_academico",
    user="postgres",
    password="AH6033"
)

cursor = conexao.cursor()

# =========================================
# FUNÇÕES
# =========================================

def cadastrar_aluno():
    print("\n=== CADASTRAR ALUNO ===")

    nome = input("Nome do aluno: ")
    cpf = input("CPF: ")
    data_nascimento = input("Data de nascimento (AAAA-MM-DD): ")

    cursor.execute(
        "SELECT cadastrar_aluno(%s, %s, %s)",
        (nome, cpf, data_nascimento)
    )

    resultado = cursor.fetchone()

    print("\n" + resultado[0])

    conexao.commit()


def cadastrar_professor():
    print("\n=== CADASTRAR PROFESSOR ===")

    nome = input("Nome do professor: ")
    cpf = input("CPF: ")
    especialidade = input("Especialidade: ")

    cursor.execute(
        "SELECT cadastrar_professor(%s, %s, %s)",
        (nome, cpf, especialidade)
    )

    resultado = cursor.fetchone()

    print("\n" + resultado[0])

    conexao.commit()


def criar_disciplina():
    print("\n=== CRIAR DISCIPLINA ===")

    nome = input("Nome da disciplina: ")
    codigo = input("Código da disciplina: ")

    cursor.execute(
        "SELECT criar_disciplina(%s, %s)",
        (nome, codigo)
    )

    resultado = cursor.fetchone()

    print("\n" + resultado[0])

    conexao.commit()


def vincular_professor_disciplina():
    print("\n=== VINCULAR PROFESSOR À DISCIPLINA ===")

    professor_id = int(input("ID do professor: "))
    disciplina_id = int(input("ID da disciplina: "))

    cursor.execute(
        "SELECT vincular_professor_turma(%s, %s)",
        (professor_id, disciplina_id)
    )

    resultado = cursor.fetchone()

    print("\n" + resultado[0])

    conexao.commit()


def listar_alunos():
    print("\n=== LISTA DE ALUNOS ===")

    cursor.execute("SELECT * FROM alunos")

    alunos = cursor.fetchall()

    for aluno in alunos:
        print(aluno)


def listar_professores():
    print("\n=== LISTA DE PROFESSORES ===")

    cursor.execute("SELECT * FROM professores")

    professores = cursor.fetchall()

    for professor in professores:
        print(professor)


def listar_disciplinas():
    print("\n=== LISTA DE DISCIPLINAS ===")

    cursor.execute("SELECT * FROM disciplinas")

    disciplinas = cursor.fetchall()

    for disciplina in disciplinas:
        print(disciplina)


# =========================================
# MENU PRINCIPAL
# =========================================

while True:

    print("\n=================================")
    print(" SISTEMA ACADÊMICO ")
    print("=================================")

    print("1 - Cadastrar aluno")
    print("2 - Cadastrar professor")
    print("3 - Criar disciplina")
    print("4 - Vincular professor à disciplina")
    print("5 - Listar alunos")
    print("6 - Listar professores")
    print("7 - Listar disciplinas")
    print("0 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        cadastrar_aluno()

    elif opcao == "2":
        cadastrar_professor()

    elif opcao == "3":
        criar_disciplina()

    elif opcao == "4":
        vincular_professor_disciplina()

    elif opcao == "5":
        listar_alunos()

    elif opcao == "6":
        listar_professores()

    elif opcao == "7":
        listar_disciplinas()

    elif opcao == "0":
        print("\nEncerrando sistema...")
        break

    else:
        print("\nOpção inválida!")

# =========================================
# FECHANDO CONEXÃO
# =========================================

cursor.close()
conexao.close()