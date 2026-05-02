from pymongo import MongoClient
from datetime import datetime

class MongoModule:
    def __init__(self):
        # Conexão técnica com o banco via driver pymongo
        self.client = MongoClient("mongodb://admin:senha@localhost:27017/")
        self.db = self.client['sistema_escolar']
        self.colecao = self.db['notas_alunos']

    def salvar_notas_com_regra(self, aluno_id, disciplina_id, p1, p2, lab, proj, p3=None):
        # Validação de campos obrigatórios
        if not aluno_id or not disciplina_id:
            return {"erro": "ID ou Disciplina inválidos"}

        # Cálculo da média inicial com as 4 avaliações
        media_inicial = (p1 + p2 + lab + proj) / 4
        
        if p3 is None:
            # Fluxo inicial: Verifica se atingiu a média 6
            if media_inicial >= 6:
                status = "Aprovado na Disciplina"
                precisa_p3 = False
                media_final = media_inicial
            else:
                status = "Em Recuperação (Precisa de P3)"
                precisa_p3 = True
                media_final = media_inicial
        else:
            # Fluxo após P3: Substitui a menor nota entre P1 e P2[cite: 1]
            if p3 > min(p1, p2):
                if p1 < p2: p1 = p3
                else: p2 = p3
            
            media_final = (p1 + p2 + lab + proj) / 4
            # Regra final de aprovação/reprovação[cite: 1]
            status = "Aprovado na Disciplina" if media_final >= 6 else "Reprovado na Disciplina"
            precisa_p3 = False

        filtro = {"aluno_id": aluno_id, "disciplina_id": disciplina_id}
        
        # Documento JSON que será persistido no MongoDB[cite: 1]
        dados = {
            "$set": {
                "avaliacoes": {"p1": p1, "p2": p2, "lab": lab, "proj": proj, "p3": p3},
                "media_final": round(media_final, 2),
                "status": status,
                "precisa_p3": precisa_p3,
                "data_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
        }
        
        self.colecao.update_one(filtro, dados, upsert=True)
        return {"media": round(media_final, 2), "status": status, "p3": precisa_p3}