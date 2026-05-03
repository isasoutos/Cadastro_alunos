import json
from database.mongo_db import MongoModule

def exibir_menu():
    print("\n" + "="*55)
    print("   SISTEMA PEDAGÓGICO - FEI (MÓDULO MONGO)   ")
    print("="*55)
    print("1. Lançar Notas com Regras (P1, P2, Lab, Proj, P3)")
    print("2. Lançar Notas Flexíveis (Qualquer formato)")
    print("3. Atualizar uma Nota Específica")
    print("4. Definir Plano de Ensino (Ementa)")
    print("5. Buscar Histórico Escolar (Boletim do Aluno)")
    print("0. Sair do Sistema")
    print("="*55)

def testar_sistema():
    db = MongoModule()
    
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '0':
            print("Encerrando o módulo MongoDB... Até logo!")
            break

        # ==========================================
        # OPÇÃO 1: REGRA DE NEGÓCIO COMPLETA (P3)
        # ==========================================
        elif opcao == '1':
            print("\n--- REGRA DE APROVAÇÃO (CÁLCULO AUTOMÁTICO) ---")
            aluno = input("ID do Aluno: ").strip()
            materia = input("Código da Disciplina: ").strip()
            
            try:
                p1 = float(input("Nota P1: "))
                p2 = float(input("Nota P2: "))
                lab = float(input("Nota Lab: "))
                proj = float(input("Nota Projeto: "))
                
                res = db.salvar_notas_com_regra(aluno, materia, p1, p2, lab, proj)
                print(f"\nSTATUS: {res['status']} | MÉDIA: {res['media']}")
                
                if res['p3']:
                    print("AVISO: Aluno abaixo da média 6!")
                    if input("Lançar P3 agora? (s/n): ").lower() == 's':
                        nota_p3 = float(input("Nota da P3: "))
                        res_f = db.salvar_notas_com_regra(aluno, materia, p1, p2, lab, proj, nota_p3)
                        print(f"\nSTATUS FINAL: {res_f['status']} | MÉDIA FINAL: {res_f['media']}")
            except ValueError:
                print("[ERRO] Digite apenas números.")

        # ==========================================
        # OPÇÃO 2: FORMATO FLEXÍVEL (JSON DINÂMICO)
        # ==========================================
        elif opcao == '2':
            print("\n--- LANÇAMENTO FLEXÍVEL (SCHEAMALESS) ---")
            aluno = input("ID do Aluno: ").strip()
            materia = input("Código da Disciplina: ").strip()
            
            notas_flex = {}
            print("Digite os nomes das avaliações e as notas (Deixe o nome em branco para parar):")
            while True:
                nome_aval = input("Nome da Avaliação (ex: Atividade_Extra): ").strip()
                if not nome_aval:
                    break
                try:
                    nota_aval = float(input(f"Nota para {nome_aval}: "))
                    notas_flex[nome_aval] = nota_aval
                except ValueError:
                    print("Nota inválida! Tente novamente.")
            
            if notas_flex:
                resultado = db.lancar_notas(aluno, materia, notas_flex)
                print(f"\n>> {resultado['mensagem']}")

        # ==========================================
        # OPÇÃO 3: ATUALIZAR NOTA ESPECÍFICA
        # ==========================================
        elif opcao == '3':
            print("\n--- ATUALIZAR NOTA ESPECÍFICA ---")
            aluno = input("ID do Aluno: ").strip()
            materia = input("Código da Disciplina: ").strip()
            nome_aval = input("Qual avaliação deseja alterar? (ex: P2): ").strip()
            
            try:
                nova_nota = float(input("Digite a nova nota: "))
                resultado = db.atualizar_nota_especifica(aluno, materia, {nome_aval: nova_nota})
                if resultado['sucesso']:
                    print(f"\n>> {resultado['mensagem']}")
                else:
                    print(f"\n[ERRO] {resultado['erro']}")
            except ValueError:
                print("[ERRO] Nota inválida!")

        # ==========================================
        # OPÇÃO 4: PLANO DE ENSINO (EMENTA)
        # ==========================================
        elif opcao == '4':
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
                resultado = db.definir_plano_ensino(materia, ementa)
                print(f"\n>> {resultado['mensagem']}")

        # ==========================================
        # OPÇÃO 5: BUSCAR HISTÓRICO (BOLETIM)
        # ==========================================
        elif opcao == '5':
            print("\n--- CONSULTAR BOLETIM ---")
            aluno = input("ID do Aluno: ").strip()
            historico = db.buscar_historico_aluno(aluno)
            
            if not historico:
                print("Nenhum registro encontrado para este aluno.")
            else:
                print("\nRegistros encontrados:")
                # Imprime o JSON de forma bonita e indentada
                print(json.dumps(historico, indent=4, ensure_ascii=False))

        else:
            print("[ERRO] Opção inválida. Tente novamente.")

if __name__ == "__main__":
    testar_sistema()