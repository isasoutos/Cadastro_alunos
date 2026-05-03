from database.mongo_db import MongoModule
from datetime import datetime

# ==========================================
# 1. MOCKS (Simuladores dos outros bancos)
# ==========================================
class PostgresMock:
    def consultar_perfil_completo(self, aluno_id):
        # Finge que foi no banco relacional do Akira
        return {"nome": "Aluno Teste", "cpf": "111.222.333-44", "matricula": aluno_id}

class Neo4jMock:
    def verificar_elegibilidade(self, aluno_id, disciplina_id):
        # Finge que navegou nos grafos da Pessoa 3
        return True 

    def sugerir_proximas_materias(self, aluno_id):
        return ["Estatística Avançada", "Machine Learning"]

class CassandraMock:
    def registrar_log_evento(self, usuario_id, acao, detalhe):
        # Finge que salvou o log na tabela wide-column da Pessoa 4
        print(f"[CASSANDRA LOG] Usuário: {usuario_id} | Ação: {acao} | Detalhe: {detalhe}")

# ==========================================
# 2. FUNÇÕES TRANSVERSAIS (Onde a mágica acontece)
# ==========================================
class SistemaIntegrado:
    def __init__(self):
        self.mongo = MongoModule()         # O SEU banco real e funcional
        self.postgres = PostgresMock()     # Fake (Akira)
        self.neo4j = Neo4jMock()           # Fake (Pessoa 3)
        self.cassandra = CassandraMock()   # Fake (Pessoa 4)

    def middleware_log(self, usuario_id, acao, detalhe):
        """Intercepta todas as requisições e envia para o Cassandra"""
        self.cassandra.registrar_log_evento(usuario_id, acao, detalhe)

    def gerar_boletim_consolidado(self, aluno_id):
        """Junta os dados dos 4 bancos em um único relatório"""
        self.middleware_log("sistema", "GERAR_BOLETIM", f"Gerando boletim para {aluno_id}")
        
        # 1. Pega o Nome no PostgreSQL (Akira)
        dados_cadastrais = self.postgres.consultar_perfil_completo(aluno_id)
        
        # 2. Pega as Notas no MongoDB (Isabelle - REAL)
        historico_notas = self.mongo.buscar_historico_aluno(aluno_id)
        
        # 3. Pega o Progresso no Neo4j (Pessoa 3)
        sugestoes = self.neo4j.sugerir_proximas_materias(aluno_id)
        
        # Constrói a resposta final que será exibida na tela
        boletim = {
            "identidade": dados_cadastrais,
            "desempenho_academico": historico_notas,
            "trilha_recomendada": sugestoes
        }
        
        return boletim

    def lancar_nota_integrada(self, prof_id, aluno_id, disciplina_id, notas):
        """Exemplo de fluxo completo antes de salvar no seu Mongo"""
        self.middleware_log(prof_id, "TENTATIVA_LANCAMENTO", f"Prof {prof_id} lançando nota para {aluno_id}")
        
        # Verifica no Neo4j se o aluno realmente tem os pré-requisitos/está cursando
        if self.neo4j.verificar_elegibilidade(aluno_id, disciplina_id):
            # Se sim, salva no seu Mongo
            resultado = self.mongo.lancar_notas(aluno_id, disciplina_id, notas)
            self.middleware_log(prof_id, "SUCESSO_LANCAMENTO", f"Notas salvas no MongoDB para {aluno_id}")
            return resultado
        else:
            self.middleware_log(prof_id, "FALHA_LANCAMENTO", f"Aluno {aluno_id} inelegível para {disciplina_id}")
            return {"erro": "Aluno não cumpre os pré-requisitos curriculares."}