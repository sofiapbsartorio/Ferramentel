from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime, timedelta
from util.validators import *


class LocacaoDTO(BaseModel):
    cliente_id: int
    data_emprestimo: date
    data_devolucao: date
    produto_id: int
    valor_total: float
    
   
