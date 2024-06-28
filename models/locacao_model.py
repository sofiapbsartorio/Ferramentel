from dataclasses import dataclass
from datetime import date
from typing import List, Optional
from models.cliente_model import Cliente

@dataclass
class Locacao:
    id: Optional[int] = None
    cliente_id: Optional[int] = None
    data_locacao: Optional[date] = None
    produto_id: Optional[int] = None