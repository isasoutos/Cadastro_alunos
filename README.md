# 🎓 Sistema Acadêmico Integrado - Persistência Poliglota

Um sistema de gestão educacional robusto desenvolvido para demonstrar o conceito prático de **Persistência Poliglota**, utilizando quatro paradigmas diferentes de bancos de dados para resolver problemas específicos e complementares de negócio dentro do mesmo ecossistema acadêmico.

## 🎯 O Tema Escolhido

No ambiente universitário, lidamos diariamente com fluxos de dados que possuem naturezas, criticidades e velocidades de alteração completamente distintas. Este projeto consolida essa dualidade através de uma arquitetura híbrida distribuída, provando que não existe um "banco de dados perfeito" universal, mas sim a ferramenta correta para cada domínio de negócio:

* **Dados Estritos e Relacionais:** Identidade de alunos, registros de professores, CPFs únicos e vínculos administrativos estáveis.
* **Dados Dinâmicos e Flexíveis:** Notas acadêmicas com múltiplos formatos de avaliação (que variam por disciplina) e planos de ensino estruturados.
* **Regras de Redes Complexas:** Dependências, pré-requisitos curriculares de avanço e sugestões de trilhas de aprendizagem.
* **Histórico Temporal de Alta Volumetria:** Trilhas imutáveis de auditoria, logs de acessos sensíveis e monitoramento de segurança.

---

## 🏗️ Arquitetura e Tecnologias (Os 4 Bancos de Dados)

O sistema utiliza **Python** como a camada middleware centralizadora (orquestrador) para conectar, processar as regras de negócio e gerenciar as conexões simultâneas entre os seguintes serviços contêinerizados via **Docker**:

### 1. PostgreSQL (Módulo de Identidade — Akira)
* **Paradigma:** Relacional (SQL).
* **Justificativa:** Focado na estrita conformidade ACID (Atomicidade, Consistência, Isolamento e Durabilidade). É o "dono" da verdade cadastral, ideal para garantir que dados fundamentais não sofram com inconsistências (como duplicidade de CPFs ou alunos sem número de matrícula).
* **Recursos:** Implementado via Procedures/Funções armazenadas nativas (`cadastrar_aluno`, `cadastrar_professor`, `criar_disciplina`, `vincular_professor_turma`).

### 2. MongoDB (Módulo Pedagógico — Isabelle)
* **Paradigma:** Orientado a Documentos (NoSQL).
* **Justificativa:** Oferece um Esquema Flexível (Schemaless). Perfeito para armazenar notas e planos de ensino, permitindo que uma disciplina salve avaliações no formato `{"P1": 8.5, "Projeto": 9.0}` e outra salve apenas `{"Seminario": 10.0, "Artigo": 7.5}` na mesma coleção, sem a necessidade de migrações complexas de tabelas.
* **Recursos:** Manipulação e gravação direta de objetos JSON complexos com controle dinâmico de médias acadêmicas e recuperação (P3).

### 3. Neo4j (Módulo de Regras Curriculares — Pessoa 3)
* **Paradigma:** Orientado a Grafos (NoSQL).
* **Justificativa:** Altamente otimizado para gerenciar relacionamentos complexos. Em vez de realizar múltiplos e lentos `JOINs` relacionais para verificar pré-requisitos encadeados (ex: IA depende de Estatística, que depende de Cálculo), o Neo4j faz uma navegação rápida por caminhos de nós de forma intuitiva.
* **Recursos:** Funções estruturadas para mapeamento de dependências (`criar_pre_requisito`), tracking de avanço (`registrar_conclusao`) e inteligência analítica (`sugerir_proximas_materias`).

### 4. Cassandra (Módulo de Auditoria e Timeline — Pessoa 4)
* **Paradigma:** Wide-Column / Colunar (NoSQL).
* **Justificativa:** Projetado para altíssima escalabilidade e velocidade extrema de escrita em séries temporais. Garante que logs de auditoria e registros de segurança sejam gravados instantaneamente de forma imutável, fornecendo rastreabilidade completa e permanente para a secretaria acadêmica.
* **Recursos:** Centralização automática de histórico de segurança (`registrar_log_evento`, `listar_auditoria_por_aluno`, `monitorar_acesso`).

---

## ⚙️ Funções Transversais e Integração (O Coração do Backend)

O backend em Python atua interceptando as requisições e cruzando dados de todos os ecossistemas de forma integrada:

1.  **Validação Cruzada de Escrita:** O sistema impede nativamente o lançamento de notas ou ementas no MongoDB se o ID do Aluno ou da Disciplina não for localizado e validado previamente na base relacional estável do PostgreSQL.
2.  **Gerar Boletim Consolidado:** Uma única chamada unificada consome o nome e dados cadastrais no *PostgreSQL*, busca as notas flexíveis no *MongoDB*, avalia o progresso curricular no grafo do *Neo4j* e valida se existem acessos ou alterações suspeitas na timeline do *Cassandra*.
3.  **Middleware de Log Automático (`middleware_log`):** Intercepta de forma invisível qualquer operação realizada no menu integrado e dispara uma gravação assíncrona para o Cassandra, gerando o rastro definitivo de auditoria sem a necessidade de acionamento manual em cada módulo.

---

## 🚀 Como Rodar o Código

Para testar o projeto, você precisará ter o **Docker** instalado na sua máquina. Siga o passo a passo abaixo no terminal (na raiz do projeto):

### Passo 1: Construir a Infraestrutura
Primeiro, vamos construir a imagem do Python e baixar as dependências:
```bash
docker-compose build --no-cache
```

### Passo 2: Ligar os Bancos de Dados
Agora, subimos os bancos PostgreSQL e MongoDB em segundo plano. (O Docker vai ler o `init.sql` e criar as tabelas do Akira automaticamente aqui):
```bash
docker-compose up -d
```

### Passo 3: Executar o Menu do Sistema
Com os bancos ligados, rode este comando para abrir o sistema interativo em Python e começar a testar:
```bash
docker-compose run app_python python main.py
```

---
💡 **Dica para parar de rodar:** Quando terminar de testar, digite `0` no menu para sair. Para desligar os bancos de dados e limpar o terminal, rode: `docker-compose down`

---
## 📂 Estrutura do Repositório

```text
├── docker-compose.yml       # Orquestração de todos os containers e volumes do ecossistema
├── init.sql                 # Script de inicialização automática de tabelas e funções do Postgres
├── README.md                # Documentação técnica completa do sistema
└── src/
    ├── Dockerfile           # Definição da imagem isolada para a aplicação Python (3.12-slim)
    ├── main.py              # Interface de Linha de Comando (CLI) centralizada com 12 opções
    ├── requirements.txt     # Dependências externas do projeto (psycopg2-binary, pymongo)
    └── database/
        ├── mongo_db.py      # Conexão e regras de negócio orientadas a documentos
        └── postgres_db.py   # Conexão e injeção de parâmetros nas funções relacionais
