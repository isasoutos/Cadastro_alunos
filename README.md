# 🎓 Sistema Acadêmico Integrado - Persistência Poliglota

Um sistema de gestão educacional robusto desenvolvido para demonstrar o conceito prático de **Persistência Poliglota**, utilizando quatro paradigmas diferentes de bancos de dados para resolver problemas específicos e complementares de negócio dentro do mesmo ecossistema acadêmico.

## 👥 Integrantes do Grupo
* **Isabelle:** Módulo Pedagógico (MongoDB)
* **Akira:** Módulo de Identidade (PostgreSQL)
* **Leonardo:** Módulo de Regras Curriculares (Neo4j)
* **Renan:** Módulo de Auditoria e Timeline (Cassandra)

---

## 🎯 O Tema Escolhido

No ambiente universitário, lidamos diariamente com fluxos de dados que possuem naturezas, criticidades e velocidades de alteração completamente distintas. Este projeto consolida essa dualidade através de uma arquitetura híbrida distribuída, provando que não existe um "banco de dados perfeito" universal, mas sim a ferramenta correta para cada domínio de negócio:

* **Dados Estritos e Relacionais:** Identidade de alunos, registros de professores, CPFs únicos e vínculos administrativos estáveis.
* **Dados Dinâmicos e Flexíveis:** Notas acadêmicas com múltiplos formatos de avaliação (que variam por disciplina) e planos de ensino estruturados.
* **Regras de Redes Complexas:** Dependências, pré-requisitos curriculares de avanço e sugestões de trilhas de aprendizagem.
* **Histórico Temporal de Alta Volumetria:** Trilhas imutáveis de auditoria, logs de acessos sensíveis e monitoramento de segurança.

## 🐍 Linguagem de Implementação

O **Python** foi a linguagem escolhida para implementar a camada middleware (orquestrador) do projeto. 
* **Justificativa:** O Python possui um ecossistema maduro com drivers oficiais e robustos para todos os bancos modernos (como `psycopg2` para Postgres e `pymongo` para MongoDB). Ele facilita a criação de uma Interface de Linha de Comando (CLI) unificada e permite o processamento ágil da validação cruzada entre os módulos (ex: validar o relacional antes de gravar no NoSQL), integrando-se nativamente à arquitetura conteinerizada do Docker.

---

## 🏗️ Arquitetura e Tecnologias (Os 4 Bancos de Dados)

O sistema utiliza Python para gerenciar as conexões simultâneas entre os seguintes serviços:

### 1. PostgreSQL (Módulo de Identidade — Akira)
* **Paradigma:** Relacional (SQL).
* **Justificativa:** Focado na estrita conformidade ACID (Atomicidade, Consistência, Isolamento e Durabilidade). É o "dono" da verdade cadastral, ideal para garantir que dados fundamentais não sofram com inconsistências (como duplicidade de CPFs ou alunos sem número de matrícula).

### 2. MongoDB (Módulo Pedagógico — Isabelle)
* **Paradigma:** Orientado a Documentos (NoSQL).
* **Justificativa:** Oferece um Esquema Flexível (Schemaless). Perfeito para armazenar notas e planos de ensino, permitindo que disciplinas salvem avaliações em formatos diferentes na mesma coleção, sem migrações complexas.

### 3. Neo4j (Módulo de Regras Curriculares — Leonardo)
* **Paradigma:** Orientado a Grafos (NoSQL).
* **Justificativa:** Altamente otimizado para gerenciar relacionamentos complexos. Substitui lentos `JOINs` relacionais por navegação rápida em caminhos de nós para validar pré-requisitos encadeados.

### 4. Cassandra (Módulo de Auditoria e Timeline — Renan)
* **Paradigma:** Wide-Column / Colunar (NoSQL).
* **Justificativa:** Projetado para altíssima escalabilidade e velocidade de escrita em séries temporais. Grava instantaneamente logs de auditoria de forma imutável, fornecendo rastreabilidade completa.

---

## ⚖️ Fundamentos Teóricos: Teorema CAP e Consistência

O sistema lida com diferentes cenários de indisponibilidade de acordo com o Teorema CAP e princípios de consistência:

* **PostgreSQL (CA):** Trabalha com **Consistência Forte (ACID)**. Em caso de falha de rede (partição), ele bloqueia gravações para evitar dados divergentes, ficando indisponível para escrita até a normalização.
* **MongoDB (CP):** Possui **Consistência Forte por padrão no nó Primário**. Se o nó líder cair, o sistema fica temporariamente indisponível para escrita durante os segundos de eleição do novo primário.
* **Neo4j (CP):** Trabalha com **Consistência Causal**. Se o nó líder falhar ou houver partição isolando a maioria, ele para de aceitar escritas para garantir a integridade estrutural do grafo.
* **Cassandra (AP):** Trabalha com **Consistência Eventual Ajustável (Tunable)**. Prioriza a disponibilidade; se nós falharem, ele continua aceitando operações, sacrificando temporariamente a consistência imediata (os dados são sincronizados no background).

## 🔄 Tolerância a Falhas e Replicação (Bancos NoSQL)

Para os bancos não-relacionais, a arquitetura distribuída lida com instâncias indisponíveis baseada no conceito de Quórum (maioria):

* **MongoDB (Replica Set):** Se o nó Primário cai, os Secundários elegem um novo líder. Em um cluster padrão de **3 instâncias, 1 pode falhar** e o sistema continuará operante e consistente.
* **Neo4j (Causal Cluster):** Utiliza o protocolo Raft. A maioria é exigida para aceitar escritas. Em um cenário com **3 servidores Core, 1 pode falhar** sem afetar a consistência.
* **Cassandra (Ring Topology):** Arquitetura masterless (sem líder). A tolerância depende do Fator de Replicação (RF) e do nível da query. Com `RF=3` e consistência de leitura/escrita em `QUORUM`, **1 instância pode falhar** mantendo consistência forte. Com nível `ONE`, **2 instâncias podem falhar**, mas o sistema passa a operar em consistência eventual pura.

---

## ⚙️ Funções Transversais e Integração (O Coração do Backend)

O backend em Python atua interceptando as requisições e cruzando dados de todos os ecossistemas:

1.  **Validação Cruzada de Escrita:** Impede o lançamento de notas no MongoDB se o ID do Aluno não for validado previamente no PostgreSQL.
2.  **Gerar Boletim Consolidado:** Uma única chamada consome o nome no *PostgreSQL*, as notas no *MongoDB*, avalia o progresso no *Neo4j* e valida acessos suspeitos no *Cassandra*.
3.  **Middleware de Log Automático (`middleware_log`):** Intercepta de forma invisível as operações no menu integrado e dispara a gravação assíncrona para o Cassandra.

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

## 💻 Acessando os Bancos e Tabelas pelo Terminal (CLI)
Após usar o menu em Python para popular o sistema, você pode auditar as tabelas e os dados acessando os contêineres diretamente.

⚠️ Atenção usuários de Windows: Se você estiver utilizando o terminal do Git Bash, é necessário adicionar a palavra winpty  antes de qualquer comando docker exec para que o terminal interativo funcione corretamente (Exemplo: winpty docker exec -it ...).

---

🐘 PostgreSQL (Cadastros Base)
Conectar ao banco de dados:

```bash
docker exec -it postgres_fei psql -U postgres -d sistema_academico
(Quando solicitado, digite a senha AH6033 — os caracteres ficam totalmente invisíveis por segurança).
````
Listar todas as tabelas existentes:

```SQL
\dt
```

Listar e Estruturar as Tabelas
Ver a lista de todas as tabelas criadas:

```SQL
\dt
```

Ver a estrutura de uma tabela específica (quais são as colunas e tipos de dados):

```SQL
\d alunos
\d professores
\d disciplinas
```

Códigos para Acessar os Dados (Os SELECTs)
Lembre-se de sempre colocar o ponto e vírgula (;) no final de cada comando!

Ver todos os Alunos cadastrados:

```SQL
SELECT * FROM alunos;
```

Ver todos os Professores cadastrados:

```SQL
SELECT * FROM professores;
```

Ver todas as Disciplinas cadastradas:

```SQL
SELECT * FROM disciplinas;
```

Encerrar a sessão e sair do contêiner:

```SQL
\q
```

--- 

🍃 MongoDB (Notas e Planos de Ensino)
Conectar ao banco de dados:

```bash
docker exec -it mongodb_fei mongosh -u admin -p admin
```

Selecionar o banco de dados do sistema:

```JavaScript
use sistema_escolar
```

Listar as coleções (equivalente às tabelas):

```JavaScript
show collections
```

Visualizar as notas salvas com formatação estruturada (JSON):

```JavaScript
db.notas_alunos.find().pretty()
```

Encerrar a sessão e sair do contêiner:

```JavaScript
exit
```

---

🕸️ Neo4j (Relacionamentos e Matrículas)
Conectar ao banco de dados:

```bash
docker exec -it neo4j_fei cypher-shell -u neo4j -p senha123
```

Visualizar todos os nós de Alunos cadastrados:

```Cypher
MATCH (a:Aluno) RETURN a;
```

Visualizar todos os relacionamentos de matrículas ativos:

```Cypher
MATCH (a:Aluno)-[r:CURSA]->(d:Disciplina) RETURN a.nome, d.nome;
```

Encerrar a sessão e sair do contêiner:

```Cypher
:exit
```
(Nota: O comando de saída do Neo4j obrigatoriamente começa com dois-pontos).

---

👁️ Cassandra (Logs de Auditoria)
Conectar ao banco de dados:

```bash
docker exec -it cassandra_fei cqlsh
```

Selecionar o Keyspace (banco de dados) do sistema:

```SQL
USE sistema_auditoria;
```

Listar as tabelas criadas no Keyspace:

```SQL
DESCRIBE TABLES;
```

Visualizar toda a trilha temporal de logs e eventos:

```SQL
SELECT * FROM logs_eventos;
```

Encerrar a sessão e sair do contêiner:

```SQL
exit
```

---

## 📂 Estrutura do Repositório

```text
├── cassandra.sql            # Consultas e estrutura nativa do Cassandra (Documentação/Backup)
├── docker-compose.yml       # Orquestração de todos os containers e volumes do ecossistema
├── init.sql                 # Script de inicialização automática de tabelas e funções do Postgres
├── notas.json               # Estrutura JSON de exemplo para o MongoDB (Documentação)
├── queries.cypher           # Comandos nativos de criação de nós do Neo4j (Documentação/Backup)
├── README.md                # Documentação técnica completa do sistema
└── src/
    ├── Dockerfile           # Definição da imagem isolada para a aplicação Python (3.12-slim)
    ├── main.py              # Interface de Linha de Comando (CLI) centralizada com 16 opções
    ├── requirements.txt     # Dependências (psycopg2-binary, pymongo, cassandra-driver, neo4j)
    └── database/
        ├── __init__.py      # Arquivo que transforma a pasta em um módulo Python reconhecido
        ├── cassandra_db.py  # Conexão e regras de log de auditoria no formato Colunar
        ├── mongo_db.py      # Conexão e regras de negócio orientadas a documentos
        ├── neo4j_db.py      # Conexão e lógica de relacionamentos em Grafos
        └── postgres_db.py   # Conexão e injeção de parâmetros nas funções relacionais
