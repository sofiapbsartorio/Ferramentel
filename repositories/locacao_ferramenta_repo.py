import sqlite3
import json
from typing import List, Optional
from models.locacao_model import Emprestimo
from models.cliente_model import Cliente
from sql.locacao_ferramentas_sql import SQL_INSERIR, SQL_CRIAR_TABELA, SQL_OBTER_QUANTIDADE
from util.database import obter_conexao

class LocacaoFerramentaRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, emprestimo_id: int, produto_id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR, (emprestimo_id, produto_id))
                if cursor.rowcount > 0:
                    return True
        except sqlite3.Error as ex:
            print(ex)
            return False
    @classmethod
    def inserir_locacao_ferramenta_json(cls, arquivo_json: str):
        try:
            if LocacaoFerramentaRepo.obter_quantidade() == 0:
                with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                    locacao = json.load(arquivo)
                    for locacao_data in locacao:
                        locacao_id = locacao_data.get('locacao_id')
                        produto_id = locacao_data.get('produto_id')
                        if produto_id is not None and produto_id is not None:
                            LocacaoFerramentaRepo.inserir(locacao_id, produto_id)

        except FileNotFoundError:
            print(f"Arquivo '{arquivo_json}' não encontrado.")
        except json.JSONDecodeError:
            print(f"Erro ao decodificar o arquivo JSON '{arquivo_json}'.")
        except sqlite3.Error as ex:
            print(f"Erro SQL ao inserir empréstimo-livro do JSON: {ex}")


    @classmethod
    def obter_quantidade(cls) -> Optional[int]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None
