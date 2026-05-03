from pymongo import MongoClient
from datetime import datetime

class MongoModule:
    def __init__(self):
        self.client = MongoClient("mongodb://admin:senha@localhost:27017/")
        self.db = self.client['sistema_escolar']
        
        # CORREÇÃO: Definindo as duas coleções corretamente aqui no início
        self.notas_colecao = self.db['notas_alunos']
        self.planos_colecao = self.db['planos_ensino']

    def salvar_notas_com_regra(self, aluno_id, disciplina_id, p1, p2, lab, proj, p3=None):
        if not aluno_id or not disciplina_id:
            return {"erro": "ID ou Disciplina inválidos"}
            
        media_inicial = (p1 + p2 + lab + proj) / 4    
        
        if p3 is None:
            if media_inicial >= 6:
                status = "Aprovado na Disciplina"
                precisa_p3 = False
                media_final = media_inicial
            else:
                status = "Em Recuperação (Precisa de P3)"
                precisa_p3 = True
                media_final = media_inicial
        else:
            if p3 > min(p1, p2):
                if p1 < p2: p1 = p3
                else: p2 = p3
            media_final = (p1 + p2 + lab + proj) / 4
            status = "Aprovado na Disciplina" if media_final >= 6 else "Reprovado na Disciplina"
            precisa_p3 = False
            
        try:
            filtro = {"aluno_id": aluno_id, "disciplina_id": disciplina_id}
            dados = {
                "$set": {
                    "avaliacoes": {"p1": p1, "p2": p2, "lab": lab, "proj": proj, "p3": p3},
                    "media_final": round(media_final, 2),
                    "status": status,
                    "precisa_p3": precisa_p3,
                    "data_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M")
                }
            }
            # Atualizado para usar notas_colecao
            self.notas_colecao.update_one(filtro, dados, upsert=True)
        except Exception:
            print("\n[AVISO] Banco MongoDB offline. Mostrando apenas cálculo local:")

        return {"media": round(media_final, 2), "status": status, "p3": precisa_p3}

    def lancar_notas(self, aluno_id, disciplina_id, objeto_notas):
        """Salva um documento JSON contendo as notas."""
        filtro = {"aluno_id": aluno_id, "disciplina_id": disciplina_id}
        dados = {
            "$set": {
                "notas": objeto_notas,
                "data_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
        }
        self.notas_colecao.update_one(filtro, dados, upsert=True)
        return {"sucesso": True, "mensagem": "Notas lançadas com sucesso!"}

    def definir_plano_ensino(self, disciplina_id, ementa):
        """Salva o conteúdo programático da disciplina."""
        filtro = {"disciplina_id": disciplina_id}
        dados = {
            "$set": {
                "ementa": ementa,
                "data_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
        }
        self.planos_colecao.update_one(filtro, dados, upsert=True)
        return {"sucesso": True, "mensagem": f"Plano de ensino de {disciplina_id} salvo."}

    def buscar_historico_aluno(self, aluno_id):
        """Recupera todos os documentos de notas vinculados àquele ID para gerar o boletim."""
        historico = list(self.notas_colecao.find({"aluno_id": aluno_id}, {"_id": 0}))
        return historico

    def atualizar_nota_especifica(self, aluno_id, disciplina_id, nova_nota):
        """Localiza o documento correto e altera apenas um campo (ex: apenas a nota da P2)."""
        campos_atualizados = {}
        for chave, valor in nova_nota.items():
            campos_atualizados[f"notas.{chave}"] = valor
            
        campos_atualizados["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")

        filtro = {"aluno_id": aluno_id, "disciplina_id": disciplina_id}
        dados = {"$set": campos_atualizados}
        
        resultado = self.notas_colecao.update_one(filtro, dados)
        
        if resultado.matched_count > 0:
            return {"sucesso": True, "mensagem": "Nota específica atualizada!"}
        else:
            return {"sucesso": False, "erro": "Aluno ou disciplina não encontrados."}