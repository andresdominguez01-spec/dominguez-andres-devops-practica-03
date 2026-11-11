# esquemas pydantic de la api: validan lo que entra y dan formato a lo que sale
from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, model_validator


# -- usuarios --
class UsuarioCreate(BaseModel):
    tipo: Literal["cliente", "administrador"]
    nombre: str = Field(min_length=1)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    direccion: Optional[str] = None  # solo es obligatoria para clientes

    @model_validator(mode="after")
    def validar_direccion(self):
        if self.tipo == "cliente" and not (self.direccion and self.direccion.strip()):
            raise ValueError("un cliente necesita direccion postal")
        return self


class UsuarioRead(BaseModel):
    id: str
    nombre: str
    email: str
    es_admin: bool


# -- productos --
class ProductoCreate(BaseModel):
    tipo: Literal["normal", "electronico", "ropa"]
    nombre: str = Field(min_length=1)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    meses_garantia: Optional[int] = Field(default=None, ge=0)  # electrónico
    talla: Optional[str] = None  # ropa
    color: Optional[str] = None  # ropa

    @model_validator(mode="after")
    def validar_atributos_por_tipo(self):
        if self.tipo == "electronico" and self.meses_garantia is None:
            raise ValueError("un producto electronico necesita meses_garantia")
        if self.tipo == "ropa" and not (self.talla and self.color):
            raise ValueError("un producto de ropa necesita talla y color")
        return self


class ProductoRead(BaseModel):
    id: str
    tipo: Literal["normal", "electronico", "ropa"]
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None


# -- pedidos --
class PedidoItemCreate(BaseModel):
    producto_id: str
    cantidad: int = Field(gt=0)


class PedidoCreate(BaseModel):
    cliente_id: str
    items: List[PedidoItemCreate] = Field(min_length=1)


class PedidoItemRead(BaseModel):
    producto_id: str
    nombre: str
    precio_unitario: float
    cantidad: int
    subtotal: float


class PedidoRead(BaseModel):
    id: str
    fecha: datetime
    cliente_id: str
    cliente_nombre: str
    total: float
    items: List[PedidoItemRead]