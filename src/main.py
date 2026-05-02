from database.mongo_db import MongoModule

def testar_sistema():
    db = MongoModule()
    
    print("="*40)
    print("   SISTEMA DE NOTAS - FEI (MÓDULO MONGO)   ")
    print("="*40)
    
    aluno = input("Digite o ID do Aluno: ").strip()
    materia = input("Digite o Código da Disciplina: ").strip()
    
    if not aluno or not materia:
        print("[ERRO] ID e Disciplina são obrigatórios!")
        return

    try:
        # Coleta inicial obrigatória[cite: 1]
        p1 = float(input("Nota P1: "))
        p2 = float(input("Nota P2: "))
        lab = float(input("Nota Lab: "))
        proj = float(input("Nota Projeto: "))
        
        # Processamento inicial[cite: 1]
        res = db.salvar_notas_com_regra(aluno, materia, p1, p2, lab, proj)
        
        print(f"\nSTATUS: {res['status']}")
        print(f"MÉDIA ATUAL: {res['media']}")
        
        # Lógica para P3[cite: 1]
        if res['p3']:
            print("\nAVISO: Aluno abaixo da média 6!")
            quer_p3 = input("Deseja lançar a nota da P3 agora? (s/n): ").lower()
            
            if quer_p3 == 's':
                nota_p3 = float(input("Nota da P3: "))
                res_f = db.salvar_notas_com_regra(aluno, materia, p1, p2, lab, proj, nota_p3)
                
                print(f"\n--- RESULTADO FINAL APÓS P3 ---")
                print(f"MÉDIA FINAL: {res_f['media']}")
                print(f"STATUS FINAL: {res_f['status']}") # Mostrará Reprovado se < 6[cite: 1]
            else:
                print("Lançamento de P3 pendente no MongoDB.")
                
    except ValueError:
        print("[ERRO] Utilize apenas números para as notas.")

if __name__ == "__main__":
    testar_sistema()