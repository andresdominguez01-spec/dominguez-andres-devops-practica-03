from typing import Dict, List, Optional

from models.pedido import Pedido
from models.producto import Producto, ProductoElectronico, ProductoRopa
from models.usuario import Administrador, Cliente, Usuario


class TiendaService:
    """clase que centraliza todas las operaciones de la tienda el cowboy espacial.

    actúa como intermediario entre los usuarios y los productos: guarda
    el inventario, los usuarios registrados y el histórico de pedidos.
    """

    def __init__(self) -> None:
        """inicializa los diccionarios y la lista que usará la tienda."""
        self.usuarios: Dict[str, Usuario] = {}
        self.productos: Dict[str, Producto] = {}
        self.pedidos: List[Pedido] = []

    def registrar_usuario(self, tipo: str, nombre: str, email: str, direccion: str = "") -> Optional[Usuario]:
        """registra un usuario nuevo en la tienda.

        el parámetro tipo puede ser "cliente" o "administrador".
        si el tipo no es correcto, devuelve none.
        """
        if tipo == "cliente":
            usuario = Cliente(nombre, email, direccion)
        elif tipo == "administrador":
            usuario = Administrador(nombre, email)
        else:
            print("tipo de usuario no válido.")
            return None

        self.usuarios[usuario.id] = usuario
        return usuario

    def anadir_producto(self, tipo: str, nombre: str, precio: float, stock: int, **kwargs) -> Optional[Producto]:
        """añade un producto nuevo al inventario de la tienda.

        el parámetro tipo puede ser "normal", "electronico" o "ropa".
        los datos extra de cada tipo (garantía, talla, color) se pasan
        con kwargs para no complicar la firma del método.
        """
        if tipo == "normal":
            producto = Producto(nombre, precio, stock)
        elif tipo == "electronico":
            producto = ProductoElectronico(nombre, precio, stock, kwargs["meses_garantia"])
        elif tipo == "ropa":
            producto = ProductoRopa(nombre, precio, stock, kwargs["talla"], kwargs["color"])
        else:
            print("tipo de producto no válido.")
            return None

        self.productos[producto.id] = producto
        return producto

    def eliminar_producto(self, producto_id: str) -> bool:
        """elimina un producto del inventario a partir de su id."""
        if producto_id in self.productos:
            del self.productos[producto_id]
            return True
        else:
            print("producto no encontrado.")
            return False

    def listar_productos(self) -> List[Producto]:
        """devuelve una lista con todos los productos disponibles en la tienda."""
        lista_productos = []
        for producto in self.productos.values():
            lista_productos.append(producto)
        return lista_productos

    def realizar_pedido(self, cliente_id: str, productos_solicitados: Dict[str, int]) -> Optional[Pedido]:
        """realiza un pedido para un cliente.

        productos_solicitados es un diccionario con id del producto y
        cantidad solicitada. primero se comprueba que el cliente existe
        y que hay stock suficiente de todo antes de descontar nada.
        """
        # comprobamos que el usuario existe y es un cliente
        if cliente_id not in self.usuarios:
            print("el usuario no existe.")
            return None

        cliente = self.usuarios[cliente_id]
        if not isinstance(cliente, Cliente):
            print("el usuario no es un cliente, no puede hacer pedidos.")
            return None

        # comprobamos que hay stock suficiente de todos los productos
        for producto_id, cantidad in productos_solicitados.items():
            if producto_id not in self.productos:
                print(f"el producto {producto_id} no existe.")
                return None

            producto = self.productos[producto_id]
            if not producto.hay_stock(cantidad):
                print(f"no hay stock suficiente de {producto.nombre}.")
                return None

        # si todo está bien, montamos el diccionario producto -> cantidad
        productos_pedido: Dict[Producto, int] = {}
        for producto_id, cantidad in productos_solicitados.items():
            producto = self.productos[producto_id]
            productos_pedido[producto] = cantidad

        # descontamos el stock de cada producto
        for producto, cantidad in productos_pedido.items():
            producto.actualizar_stock(-cantidad)

        # creamos el pedido y lo guardamos en el histórico
        nuevo_pedido = Pedido(cliente, productos_pedido)
        self.pedidos.append(nuevo_pedido)
        return nuevo_pedido

    def listar_pedidos_usuario(self, usuario_id: str) -> List[Pedido]:
        """devuelve los pedidos de un usuario ordenados por fecha."""
        pedidos_usuario = []
        for pedido in self.pedidos:
            if pedido.cliente.id == usuario_id:
                pedidos_usuario.append(pedido)

        pedidos_usuario.sort(key=lambda pedido: pedido.fecha)
        return pedidos_usuario