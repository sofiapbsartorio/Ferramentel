SQL_CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS locacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data_emprestimo DATE NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES cliente (id)
)
"""

SQL_INSERIR = """
INSERT INTO locacao(cliente_id, data_emprestimo)
VALUES (?, ?)
"""

SQL_OBTER_QUANTIDADE = """
SELECT COUNT(*) FROM locacao
"""

SQL_OBTER_TODOS = """   
SELECT * FROM locacao
ORDER BY ID

"""