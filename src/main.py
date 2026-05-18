import json

from database.mongo_db import MongoModule
from database.postgres_db import PostgresModule

# ==========================================
# NEO4J
# ==========================================

from database.neo4j_db import (
    criar_pre_requisito,
    sugerir_proximas_materias
)

# ==========================================
# CASSANDRA
# ==========================================

from database.cassandra_db import (
    registrar_log_evento,
    listar_auditoria_por_aluno,
    monitorar_acesso
)

# ==========================================
# UUID FIXO PARA TESTES
# ==========================================

USUARIO_ADMIN = "987e6543-e21b-12d3-a456-426614174999"
ALUNO_AUDITORIA = "123e4567-e89b-12d3-a456-426614174000"

# ==========================================
# MENU
# ==========================================

def exibir_menu():

    print("\n" + "="*60)
    print("="*60)

    print("1. Cadastrar Aluno")
    print("2. Cadastrar Professor")
    print("3. Criar Disciplina")
    print("4. Vincular Professor à Disciplina")

    print("5. Listar Alunos")
    print("6. Listar Professores")
    print("7. Listar Disciplinas")

    print("8. Lançar Notas com Regras")
    print("9. Lançar Notas Flexíveis")
    print("10. Atualizar uma Nota Específica")
    print("11. Definir Plano de Ensino")
    print("12. Buscar Histórico Escolar")

    # ==========================================
    # NEO4J
    # ==========================================

    print("13. Configurar Pré-Requisito")
    print("14. Ver Matérias Sugeridas")

    # ==========================================
    # CASSANDRA
    # ==========================================

    print("15. Consultar Auditoria do Aluno")
    print("16. Monitorar Acesso Sensível")

    print("\n0. Sair do Sistema")

    print("="*60)

# ==========================================
# SISTEMA PRINCIPAL
# ==========================================

def testar_sistema():

    mongo_db = MongoModule()

    try:

        postgres_db = PostgresModule()

    except Exception as e:

        print(f"[AVISO] Não foi possível conectar ao PostgreSQL: {e}")

        postgres_db = None

    while True:

        exibir_menu()

        opcao = input("Escolha uma opção: ").strip()

        # ==========================================
        # SAIR
        # ==========================================

        if opcao == '0':

            print("\nEncerrando o sistema integrado... Até logo!")

            break

        # ==========================================
        # CADASTRAR ALUNO
        # ==========================================

        elif opcao == '1':

            print("\n--- CADASTRAR ALUNO ---")

            nome = input("Nome do aluno: ").strip()

            cpf = input("CPF (apenas números): ").strip()

            nascimento = input(
                "Data de nascimento (AAAA-MM-DD): "
            ).strip()

            if postgres_db:

                msg = postgres_db.cadastrar_aluno(
                    nome,
                    cpf,
                    nascimento
                )

                print(f"\n>> {msg}")

                # ==========================================
                # CASSANDRA
                # ==========================================

                registrar_log_evento(
                    aluno_id=ALUNO_AUDITORIA,
                    usuario_id=USUARIO_ADMIN,
                    acao="CADASTRAR_ALUNO",
                    detalhe=f"Aluno {nome} cadastrado"
                )

            else:

                print("PostgreSQL offline.")

        # ==========================================
        # CADASTRAR PROFESSOR
        # ==========================================

        elif opcao == '2':

            print("\n--- CADASTRAR PROFESSOR ---")

            nome = input("Nome do professor: ").strip()

            cpf = input("CPF (apenas números): ").strip()

            especialidade = input(
                "Especialidade: "
            ).strip()

            if postgres_db:

                msg = postgres_db.cadastrar_professor(
                    nome,
                    cpf,
                    especialidade
                )

                print(f"\n>> {msg}")

                registrar_log_evento(
                    aluno_id=ALUNO_AUDITORIA,
                    usuario_id=USUARIO_ADMIN,
                    acao="CADASTRAR_PROFESSOR",
                    detalhe=f"Professor {nome} cadastrado"
                )

            else:

                print("PostgreSQL offline.")

        # ==========================================
        # CRIAR DISCIPLINA
        # ==========================================

        elif opcao == '3':

            print("\n--- CRIAR DISCIPLINA ---")

            nome = input("Nome da disciplina: ").strip()

            codigo = input(
                "Código da disciplina: "
            ).strip()

            if postgres_db:

                msg = postgres_db.criar_disciplina(
                    nome,
                    codigo
                )

                print(f"\n>> {msg}")

                registrar_log_evento(
                    aluno_id=ALUNO_AUDITORIA,
                    usuario_id=USUARIO_ADMIN,
                    acao="CRIAR_DISCIPLINA",
                    detalhe=f"Disciplina {codigo} criada"
                )

            else:

                print("PostgreSQL offline.")

        # ==========================================
        # VINCULAR PROFESSOR
        # ==========================================

        elif opcao == '4':

            print("\n--- VINCULAR PROFESSOR À DISCIPLINA ---")

            try:

                prof_id = int(
                    input("ID do professor: ")
                )

                disc_id = int(
                    input("ID da disciplina: ")
                )

                if postgres_db:

                    msg = postgres_db.vincular_professor_turma(
                        prof_id,
                        disc_id
                    )

                    print(f"\n>> {msg}")

                    registrar_log_evento(
                        aluno_id=ALUNO_AUDITORIA,
                        usuario_id=USUARIO_ADMIN,
                        acao="VINCULAR_PROFESSOR",
                        detalhe=f"Professor {prof_id} vinculado à disciplina {disc_id}"
                    )

                else:

                    print("PostgreSQL offline.")

            except ValueError:

                print("[ERRO] IDs inválidos.")

        # ==========================================
        # LISTAR ALUNOS
        # ==========================================

        elif opcao == '5':

            print("\n--- LISTA DE ALUNOS ---")

            if postgres_db:

                alunos = postgres_db.listar_alunos()

                for al in alunos:

                    print(
                        f"ID: {al[0]} | Nome: {al[1]}"
                    )

            else:

                print("PostgreSQL offline.")

        # ==========================================
        # LISTAR PROFESSORES
        # ==========================================

        elif opcao == '6':

            print("\n--- LISTA DE PROFESSORES ---")

            if postgres_db:

                profs = postgres_db.listar_professores()

                for prof in profs:

                    print(
                        f"ID: {prof[0]} | Nome: {prof[1]}"
                    )

            else:

                print("PostgreSQL offline.")

        # ==========================================
        # LISTAR DISCIPLINAS
        # ==========================================

        elif opcao == '7':

            print("\n--- LISTA DE DISCIPLINAS ---")

            if postgres_db:

                discs = postgres_db.listar_disciplinas()

                for disc in discs:

                    print(
                        f"ID: {disc[0]} | Nome: {disc[1]}"
                    )

            else:

                print("PostgreSQL offline.")

        # ==========================================
        # LANÇAR NOTAS
        # ==========================================

        elif opcao == '8':

            print("\n--- LANÇAR NOTAS ---")

            aluno = input(
                "ID do Aluno: "
            ).strip()

            materia = input(
                "Código da Disciplina: "
            ).strip()

            try:

                p1 = float(input("Nota P1: "))
                p2 = float(input("Nota P2: "))
                lab = float(input("Nota Lab: "))
                proj = float(input("Nota Projeto: "))

                res = mongo_db.salvar_notas_com_regra(
                    aluno,
                    materia,
                    p1,
                    p2,
                    lab,
                    proj
                )

                print(
                    f"\nSTATUS: {res['status']} | MÉDIA: {res['media']}"
                )

                registrar_log_evento(
                    aluno_id=ALUNO_AUDITORIA,
                    usuario_id=USUARIO_ADMIN,
                    acao="LANCAR_NOTA",
                    detalhe=f"Notas lançadas em {materia}"
                )

            except ValueError:

                print("[ERRO] Utilize apenas números.")

        # ==========================================
        # NOTAS FLEXÍVEIS
        # ==========================================

        elif opcao == '9':

            print("\n--- LANÇAMENTO FLEXÍVEL ---")

            aluno = input("ID do Aluno: ").strip()

            materia = input(
                "Código da Disciplina: "
            ).strip()

            notes_flex = {}

            while True:

                nome_aval = input(
                    "Nome da avaliação: "
                ).strip()

                if not nome_aval:

                    break

                nota_aval = float(
                    input("Nota: ")
                )

                notes_flex[nome_aval] = nota_aval

            resultado = mongo_db.lancar_notas(
                aluno,
                materia,
                notes_flex
            )

            print(f"\n>> {resultado['mensagem']}")

            registrar_log_evento(
                aluno_id=ALUNO_AUDITORIA,
                usuario_id=USUARIO_ADMIN,
                acao="LANCAR_NOTA_FLEXIVEL",
                detalhe=f"Notas flexíveis lançadas em {materia}"
            )

        # ==========================================
        # ALTERAR NOTA
        # ==========================================

        elif opcao == '10':

            print("\n--- ALTERAR NOTA ---")

            aluno = input("ID do Aluno: ").strip()

            materia = input(
                "Código da Disciplina: "
            ).strip()

            nome_aval = input(
                "Qual avaliação deseja alterar?: "
            ).strip()

            try:

                nova_nota = float(
                    input("Nova nota: ")
                )

                resultado = mongo_db.atualizar_nota_especifica(
                    aluno,
                    materia,
                    {nome_aval: nova_nota}
                )

                # Verifica se a chave "sucesso" é True
                if resultado.get("sucesso"):
                    print(f"\n>> {resultado['mensagem']}")
                    
                    registrar_log_evento(
                        aluno_id=ALUNO_AUDITORIA,
                        usuario_id=USUARIO_ADMIN,
                        acao="ALTERAR_NOTA",
                        detalhe=f"{nome_aval} alterada para {nova_nota}"
                    )
                else:
                    # Se não deu certo, imprime a chave "erro"
                    print(f"\n[ERRO] {resultado['erro']}")
                    
            except ValueError:
                print("[ERRO] Nota inválida.")

        # ==========================================
        # DEFINIR EMENTA
        # ==========================================

        elif opcao == '11':

            print("\n--- DEFINIR EMENTA ---")

            materia = input(
                "Código da Disciplina: "
            ).strip()

            ementa = []

            while True:

                topico = input(
                    f"Tópico {len(ementa)+1}: "
                ).strip()

                if not topico:

                    break

                ementa.append(topico)

            if ementa:

                resultado = mongo_db.definir_plano_ensino(
                    materia,
                    ementa
                )

                print(f"\n>> {resultado['mensagem']}")

                registrar_log_evento(
                    aluno_id=ALUNO_AUDITORIA,
                    usuario_id=USUARIO_ADMIN,
                    acao="DEFINIR_EMENTA",
                    detalhe=f"Ementa definida para {materia}"
                )

        # ==========================================
        # HISTÓRICO
        # ==========================================

        elif opcao == '12':

            print("\n--- HISTÓRICO ESCOLAR ---")

            aluno = input("ID do Aluno: ").strip()

            historico = mongo_db.buscar_historico_aluno(
                aluno
            )

            if not historico:

                print(
                    "Nenhum registro encontrado."
                )

            else:

                print(
                    json.dumps(
                        historico,
                        indent=4,
                        ensure_ascii=False
                    )
                )

                registrar_log_evento(
                    aluno_id=ALUNO_AUDITORIA,
                    usuario_id=USUARIO_ADMIN,
                    acao="CONSULTAR_HISTORICO",
                    detalhe=f"Consulta do histórico do aluno {aluno}"
                )

        # ==========================================
        # NEO4J
        # ==========================================

        elif opcao == '13':

            print("\n--- CONFIGURAR PRÉ-REQUISITO ---")

            origem = input(
                "Código da disciplina origem: "
            ).strip()

            destino = input(
                "Código da disciplina destino: "
            ).strip()

            try:

                criar_pre_requisito(
                    origem,
                    destino
                )

                print(
                    "\n>> Pré-requisito configurado."
                )

                registrar_log_evento(
                    aluno_id=ALUNO_AUDITORIA,
                    usuario_id=USUARIO_ADMIN,
                    acao="CRIAR_PRE_REQUISITO",
                    detalhe=f"{origem} -> {destino}"
                )

            except Exception as e:

                print(f"[ERRO] {e}")

        elif opcao == '14':

            print("\n--- MATÉRIAS SUGERIDAS ---")

            aluno = input(
                "ID do Aluno: "
            ).strip()

            try:

                sugestoes = sugerir_proximas_materias(
                    aluno
                )

                print("\nMatérias recomendadas:")

                for sg in sugestoes:

                    print(
                        f"Código: {sg['codigo']} | Nome: {sg['nome']}"
                    )

                registrar_log_evento(
                    aluno_id=ALUNO_AUDITORIA,
                    usuario_id=USUARIO_ADMIN,
                    acao="SUGERIR_DISCIPLINAS",
                    detalhe=f"Sugestões geradas para aluno {aluno}"
                )

            except Exception as e:

                print(f"[ERRO] {e}")

        # ==========================================
        # CASSANDRA
        # ==========================================

        elif opcao == '15':

            print("\n--- AUDITORIA DO ALUNO ---")

            aluno = input(
                "UUID do aluno: "
            ).strip()

            listar_auditoria_por_aluno(
                aluno
            )

        elif opcao == '16':

            print("\n--- MONITORAR ACESSO ---")

            endpoint = input(
                "Endpoint acessado: "
            ).strip()

            monitorar_acesso(
                usuario_id=USUARIO_ADMIN,
                endpoint=endpoint
            )

        # ==========================================
        # OPÇÃO INVÁLIDA
        # ==========================================

        else:

            print("\n[ERRO] Opção inválida.")

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    testar_sistema()