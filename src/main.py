import json
from database.mongo_db import MongoModule
from database.postgres_db import PostgresModule
from neo4j_db import criar_pre_requisito, sugerir_proximas_materias

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
    print("8. Lançar Notas com Regras (P1, P2, Lab, Proj, P3)")
    print("9. Lançar Notas Flexíveis (Qualquer formato)")
    print("10. Atualizar uma Nota Específica")
    print("11. Definir Plano de Ensino (Ementa)")
    print("12. Buscar Histórico Escolar (Boletim do Aluno)") 
    print("13. Configurar Pré-Requisito de Disciplina")
    print("14. Ver Matérias Sugeridas")
    print("\n0. Sair do Sistema")
    print("="*60)

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

        if opcao == '0':
            print("\nEncerrando o sistema integrado... Até logo!")
            break
        elif opcao == '1':
            print("\n--- CADASTRAR ALUNO ---")
            nome = input("Nome do aluno: ").strip()
            cpf = input("CPF (apenas números): ").strip()
            nascimento = input("Data de nascimento (AAAA-MM-DD): ").strip()
            if postgres_db:
                msg = postgres_db.cadastrar_aluno(nome, cpf, nascimento)
                print(f"\n>> {msg}")
            else:
                print("PostgreSQL offline.")

        elif opcao == '2':
            print("\n--- CADASTRAR PROFESSOR ---")
            nome = input("Nome do professor: ").strip()
            cpf = input("CPF (apenas números): ").strip()
            especialidade = input("Especialidade: ").strip()
            if postgres_db:
                msg = postgres_db.cadastrar_professor(nome, cpf, especialidade)
                print(f"\n>> {msg}")
            else:
                print("PostgreSQL offline.")

        elif opcao == '3':
            print("\n--- CRIAR DISCIPLINA ---")
            nome = input("Nome da disciplina: ").strip()
            codigo = input("Código da disciplina: ").strip()
            if postgres_db:
                msg = postgres_db.criar_disciplina(nome, codigo)
                print(f"\n>> {msg}")
            else:
                print("PostgreSQL offline.")

        elif opcao == '4':
            print("\n--- VINCULAR PROFESSOR À DISCIPLINA ---")
            try:
                prof_id = int(input("ID do professor: "))
                disc_id = int(input("ID da disciplina: "))
                if postgres_db:
                    msg = postgres_db.vincular_professor_turma(prof_id, disc_id)
                    print(f"\n>> {msg}")
                else:
                    print("PostgreSQL offline.")
            except ValueError:
                print("[ERRO] Os IDs devem ser números inteiros.")

        elif opcao == '5':
            print("\n--- LISTA DE ALUNOS ---")
            if postgres_db:
                alunos = postgres_db.listar_alunos()
                for al in alunos:
                    print(f"ID: {al[0]} | Nome: {al[1]} | CPF: {al[2]} | Nasc: {al[3]}")
            else:
                print("PostgreSQL offline.")

        elif opcao == '6':
            print("\n--- LISTA DE PROFESSORES ---")
            if postgres_db:
                profs = postgres_db.listar_professores()
                for prof in profs:
                    print(f"ID: {prof[0]} | Nome: {prof[1]} | CPF: {prof[2]} | Esp: {prof[3]}")
            else:
                print("PostgreSQL offline.")

        elif opcao == '7':
            print("\n--- LISTA DE DISCIPLINAS ---")
            if postgres_db:
                discs = postgres_db.listar_disciplinas()
                for disc in discs:
                    print(f"ID: {disc[0]} | Nome: {disc[1]} | Código: {disc[2]}")
            else:
                print("PostgreSQL offline.")

        elif opcao == '8':
            print("\n--- REGRA DE APROVAÇÃO (CÁLCULO AUTOMÁTICO) ---")
            aluno = input("ID do Aluno (Cadastrado no Postgres): ").strip()
            
            if postgres_db:
                alunos_validos = [str(al[0]) for al in postgres_db.listar_alunos()]
                if aluno not in alunos_validos:
                    print(f"\n[BLOQUEADO] Aluno ID {aluno} não encontrado no PostgreSQL.")
                    print("Insira as notas apenas de alunos existentes na base relacional.")
                    continue
            
            materia = input("Código da Disciplina: ").strip()
            try:
                p1 = float(input("Nota P1: "))
                p2 = float(input("Nota P2: "))
                lab = float(input("Nota Lab: "))
                proj = float(input("Nota Projeto: "))
                
                res = mongo_db.salvar_notas_com_regra(aluno, materia, p1, p2, lab, proj)
                print(f"\nSTATUS: {res['status']} | MÉDIA: {res['media']}")
                
                if res['p3']:
                    print("\nAVISO: Aluno abaixo da média 6!")
                    if input("Deseja lançar a nota da P3 agora? (s/n): ").lower() == 's':
                        nota_p3 = float(input("Nota da P3: "))
                        res_f = mongo_db.salvar_notas_com_regra(aluno, materia, p1, p2, lab, proj, nota_p3)
                        print(f"\n--- RESULTADO FINAL APÓS P3 ---")
                        print(f"MÉDIA FINAL: {res_f['media']}")
                        print(f"STATUS FINAL: {res_f['status']}")
            except ValueError:
                print("[ERRO] Utilize apenas números para as notas.")

        elif opcao == '9':
            print("\n--- LANÇAMENTO FLEXÍVEL (SCHEAMALESS) ---")
            aluno = input("ID do Aluno (Cadastrado no Postgres): ").strip()
            
            if postgres_db:
                alunos_validos = [str(al[0]) for al in postgres_db.listar_alunos()]
                if aluno not in alunos_validos:
                    print(f"\n[BLOQUEADO] Aluno ID {aluno} não encontrado no PostgreSQL.")
                    continue
                    
            materia = input("Código da Disciplina: ").strip()
            notes_flex = {}
            print("Digite os nomes das avaliações e as notas (Deixe o nome em branco para parar):")
            while True:
                nome_aval = input("Nome da Avaliação (ex: Atividade_Extra): ").strip()
                if not nome_aval:
                    break
                try:
                    nota_aval = float(input(f"Nota para {nome_aval}: "))
                    notes_flex[nome_aval] = nota_aval
                except ValueError:
                    print("Nota inválida! Tente novamente.")
            
            if notes_flex:
                resultado = mongo_db.lancar_notas(aluno, materia, notes_flex)
                print(f"\n>> {resultado['mensagem']}")

        elif opcao == '10':
            print("\n--- ATUALIZAR NOTA ESPECÍFICA ---")
            aluno = input("ID do Aluno (Cadastrado no Postgres): ").strip()
            
            if postgres_db:
                alunos_validos = [str(al[0]) for al in postgres_db.listar_alunos()]
                if aluno not in alunos_validos:
                    print(f"\n[BLOQUEADO] Aluno ID {aluno} não encontrado no PostgreSQL.")
                    continue
                    
            materia = input("Código da Disciplina: ").strip()
            nome_aval = input("Qual avaliação deseja alterar? (ex: P2): ").strip()
            try:
                nova_nota = float(input("Digite a nova nota: "))
                resultado = mongo_db.atualizar_nota_especifica(aluno, materia, {nome_aval: nova_nota})
                if resultado['sucesso']:
                    print(f"\n>> {resultado['mensagem']}")
                else:
                    print(f"\n[ERRO] {resultado['erro']}")
            except ValueError:
                print("[ERRO] Nota inválida!")

        elif opcao == '11':
            print("\n--- DEFINIR PLANO DE ENSINO ---")
            materia = input("Código da Disciplina: ").strip()
            print("Digite os tópicos da ementa (Deixe em branco para finalizar):")
            ementa = []
            while True:
                topico = input(f"Tópico {len(ementa)+1}: ").strip()
                if not topico:
                    break
                ementa.append(topico)
            
            if ementa:
                resultado = mongo_db.definir_plano_ensino(materia, ementa)
                print(f"\n>> {resultado['mensagem']}")

        elif opcao == '12':
            print("\n--- CONSULTAR BOLETIM ---")
            aluno = input("ID do Aluno: ").strip()
            historico = mongo_db.buscar_historico_aluno(aluno)
            
            if not historico:
                print("Nenhum registro encontrado para este aluno no MongoDB.")
            else:
                print("\nRegistros encontrados:")
                print(json.dumps(historico, indent=4, ensure_ascii=False))

        elif opcao == '13':
            print("\n--- CONFIGURAR PRÉ-REQUISITO ---")
            origem = input("Código da disciplina de origem: ").strip()
            destino = input("Código da disciplina de destino: ").strip()
            try:
                criar_pre_requisito(origem, destino)
                print("\n>> Pré-requisito configurado com sucesso.")
            except Exception as e:
                print(f"[ERRO] Ocorreu um erro: {e}")

        elif opcao == '14':
            print("\n--- MATÉRIAS SUGERIDAS ---")
            aluno = input("ID do Aluno: ").strip()
            try:
                sugestoes = sugerir_proximas_materias(aluno)
                print("\nMatérias recomendadas:")
                for sg in sugestoes:
                    print(f"Código: {sg['codigo']} | Nome: {sg['nome']}")
            except Exception as e:
                print(f"[ERRO] Ocorreu um erro: {e}")

        else:
            print("\n[ERRO] Opção inválida. Tente novamente.")

if __name__ == "__main__":
    testar_sistema()
