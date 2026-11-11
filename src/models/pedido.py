import uuid
from datetime import datetime
from typing import Dict

from models.producto import Producto
from models.usuario import Cliente


class Pedido:
    """representa un pedido realizado por un cliente de la tienda.

    un pedido guarda quién lo ha hecho (un cliente), qué productos ha
    pedido y en qué cantidad, y calcula el importe total de la compra.
    """

    def __init__(self, cliente: Cliente, productos: Dict[Producto, int]) -> None:
        """crea un pedido nuevo con id único y fecha automática."""
        self.id: str = str(uuid.uuid4())
        self.cliente: Cliente = cliente
        self.productos: Dict[Producto, int] = productos
        self.fecha: datetime = datetime.now()
        self.total: float = self.calcular_total()

    def calcular_total(self) -> float:
        """calcula el importe total del pedido recorriendo los productos."""
        total = 0.0
        for producto, cantidad in self.productos.items():
            total = total + (producto.precio * cantidad)
        return total

    def __str__(self) -> str:
        """devuelve un resumen legible del pedido para mostrar en consola."""
        fecha_texto = self.fecha.strftime("%d/%m/%Y %H:%M")
        texto = (
            f"pedido [{self.id[:8]}] - cliente: {self.cliente.nombre} - "
            f"fecha: {fecha_texto} - total: {self.total}€"
        )
        return texto