CREATE (:Aluno {id: "aluno_1"}) CREATE (:Aluno {id: "aluno_2"}) CREATE (:Disciplina {codigo: "CALC1", nome: "Cálculo I"}) CREATE (:Disciplina {codigo: "ESTAT", nome: "Estatística"}) CREATE (:Disciplina {codigo: "IA", nome: "Inteligência Artificial"})


MATCH (c1:Disciplina {codigo: "CALC1"}), (est:Disciplina {codigo: "ESTAT"}), (ia:Disciplina {codigo: "IA"}), (a1:Aluno {id: "aluno_1"}), (a2:Aluno {id: "aluno_2"}) MERGE (c1)-[:EH_REQUISITO_DE]->(est) MERGE (est)-[:EH_REQUISITO_DE]->(ia) MERGE (a1)-[:CONCLUIU]->(c1) MERGE (a1)-[:CONCLUIU]->(est) MERGE (a2)-[:CONCLUIU]->(c1)


MATCH (n) RETURN n


MATCH (d:Disciplina) WHERE NOT (:Aluno {id: "aluno_1"})-[:CONCLUIU]->(d) AND ALL(req IN [(r)-[:EH_REQUISITO_DE]->(d) | r] WHERE (:Aluno {id: "aluno_1"})-[:CONCLUIU]->(req)) RETURN d.codigo AS codigo, d.nome AS nome


MATCH (d:Disciplina) WHERE NOT (:Aluno {id: "aluno_2"})-[:CONCLUIU]->(d) AND ALL(req IN [(r)-[:EH_REQUISITO_DE]->(d) | r] WHERE (:Aluno {id: "aluno_2"})-[:CONCLUIU]->(req)) RETURN d.codigo AS codigo, d.nome AS nome
