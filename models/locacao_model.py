from dataclasses import dataclass
from datetime import date
from typing import List, Optional
from models.cliente_model import Cliente
from models.produto_model import Produto

@dataclass
class Locacao:
    id: Optional[int] = None
    cliente_id: Optional[int] = None
    data_emprestimo: Optional[date] = None
    data_devolucao: Optional[date] = None
    produto_id: Optional[int] = None
    valor_total: Optional[float] = None