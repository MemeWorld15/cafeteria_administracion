from pydantic import BaseModel
from typing import List, Optional

class ProductoOrden(BaseModel):
    nombre: str
    cantidad: int
    precio: float

class OrdenEntrada(BaseModel):
    cliente: str
    nota: str = ""
    usuario_id: Optional[int]
    turno: str
    productos: List[ProductoOrden]
