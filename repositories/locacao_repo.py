import sqlite3
import json

from typing import Optional, List
from models.locacao_model import Locacao
from sql.locacao_sql import *
from util.database import obter_conexao

class LocacaoRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, locacao: Locacao) -> Optional[Locacao]:
        try:
    
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR, (
                    locacao.cliente_id,
                    locacao.data_emprestimo,
                    locacao.data_devolucao,
                    locacao.produto_id,
                    locacao.valor_total,
                ))
                if cursor.rowcount > 0:
                    locacao.id = cursor.lastrowid
                    return locacao
        except sqlite3.Error as ex:
            print(ex)
            return None
    @classmethod
    def inserir_locacao_json(cls, arquivo_json: str):
        if LocacaoRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                locacoes = json.load(arquivo)
                for locacao in locacoes:
                    LocacaoRepo.inserir(Locacao(**locacao))

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

    @classmethod
    def obter_todos(cls) -> List[Locacao]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
                locacao = [Locacao(*t) for t in tuplas]
                return locacao
        except sqlite3.Error as ex:
            print(ex)
            return None


