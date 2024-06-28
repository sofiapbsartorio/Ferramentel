from dataclasses import dataclass
from models.locacao_model import Locacao
from typing import List, Optional


@dataclass
class LocacaoFerramenta:
    id: Optional[int] = None
    locacao_id: Optional[int] = None
    produto_id: Optional[int] = None
    