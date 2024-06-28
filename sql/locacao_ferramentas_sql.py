SQL_CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS locacao_ferramentas (
    locacao_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    PRIMARY KEY (locacao_id, produto_id),
    FOREIGN KEY (locacao_id) REFERENCES locacao (id),
    FOREIGN KEY (produto_id) REFERENCES produto (id)
)
"""


SQL_INSERIR = """
INSERT INTO locacao_ferramentas(locacao_id, produto_id)
VALUES (?, ?)
"""


SQL_OBTER_QUANTIDADE = """
SELECT COUNT(*) FROM locacao_ferramentas
"""