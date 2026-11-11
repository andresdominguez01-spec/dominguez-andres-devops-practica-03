# main.py: aquí van los endpoints de la api. toda la lógica de la tienda
# la hace TiendaService, esto solo recibe peticiones y devuelve respuestas.
#
# para arrancarla (desde la carpeta tienda_online):
#   uvicorn main:app --reload                      -> solo en este equipo
#   uvicorn main:app --host 0.0.0.0 --port 8000    -> accesible desde la red local
from typing import Dict, List

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from models.pedido import Pedido
from models.producto import Producto, ProductoElectronico, ProductoRopa
from models.usuario import Cliente, Usuario
from schemas import (
    PedidoCreate,
    PedidoItemRead,
    PedidoRead,
    ProductoCreate,
    ProductoRead,
    UsuarioCreate,
    UsuarioRead,
)
from services.tienda_service import TiendaService

app = FastAPI(title="API Tienda El Cowboy Espacial", version="1.0")

# cors: sin esto el navegador bloquea las peticiones del frontend a la api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# una sola tienda para todos los clientes. los datos están en memoria,
# así que se pierden al parar el servidor
tienda = TiendaService()


# datos de ejemplo para que la api no arranque vacía y se pueda comprobar
# todo desde el primer momento (en /docs, con el cliente o en el frontend)
def cargar_datos_iniciales():
    # usuarios
    spike = tienda.registrar_usuario(
        "cliente", "Spike Spiegel", "spike@bebop.com", "Calle Bebop 5, Vigo"
    )
    jimmy = tienda.registrar_usuario(
        "cliente", "Jimmy McGill", "jimmy@saulgoodman.com", "Calle Central 9, Albuquerque"
    )

    # productos
    bluray = tienda.anadir_producto(
        "electronico", "Reproductor de Blu-ray", 89.90, 10, meses_garantia=24
    )
    camiseta_bebop = tienda.anadir_producto(
        "ropa", "Camiseta Cowboy Bebop", 22.95, 15, talla="M", color="negro"
    )
    poster = tienda.anadir_producto("normal", "Poster de cine", 9.50, 30)
    camiseta_saul = tienda.anadir_producto(
        "ropa", "Camiseta Better Call Saul", 24.95, 20, talla="XL", color="azul"
    )

    # pedidos (el servicio descuenta el stock solo)
    tienda.realizar_pedido(spike.id, {bluray.id: 1, poster.id: 2})
    tienda.realizar_pedido(jimmy.id, {camiseta_saul.id: 1, poster.id: 1})


cargar_datos_iniciales()


# -- pasar de objetos de la práctica 1 a esquemas --
def usuario_a_read(usuario: Usuario) -> UsuarioRead:
    return UsuarioRead(
        id=usuario.id,
        nombre=usuario.nombre,
        email=usuario.email,
        es_admin=usuario.is_admin(),
    )


def producto_a_read(producto: Producto) -> ProductoRead:
    # miramos de qué clase es para saber el tipo
    if isinstance(producto, ProductoElectronico):
        tipo = "electronico"
    elif isinstance(producto, ProductoRopa):
        tipo = "ropa"
    else:
        tipo = "normal"
    # getattr devuelve none si el producto no tiene ese atributo
    return ProductoRead(
        id=producto.id,
        tipo=tipo,
        nombre=producto.nombre,
        precio=producto.precio,
        stock=producto.stock,
        meses_garantia=getattr(producto, "meses_garantia", None),
        talla=getattr(producto, "talla", None),
        color=getattr(producto, "color", None),
    )


def pedido_a_read(pedido: Pedido) -> PedidoRead:
    # una línea por cada producto del pedido
    items = [
        PedidoItemRead(
            producto_id=producto.id,
            nombre=producto.nombre,
            precio_unitario=producto.precio,
            cantidad=cantidad,
            subtotal=round(producto.precio * cantidad, 2),
        )
        for producto, cantidad in pedido.productos.items()
    ]
    return PedidoRead(
        id=pedido.id,
        fecha=pedido.fecha,
        cliente_id=pedido.cliente.id,
        cliente_nombre=pedido.cliente.nombre,
        total=round(pedido.total, 2),
        items=items,
    )


# -- usuarios --
@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: UsuarioCreate):
    # no dejamos crear dos usuarios con el mismo email
    if any(u.email.lower() == datos.email.lower() for u in tienda.usuarios.values()):
        raise HTTPException(status_code=409, detail="ya existe un usuario con ese email")
    usuario = tienda.registrar_usuario(
        datos.tipo, datos.nombre, datos.email, datos.direccion or ""
    )
    if usuario is None:
        raise HTTPException(status_code=400, detail="tipo de usuario no valido")
    return usuario_a_read(usuario)


@app.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios():
    return [usuario_a_read(u) for u in tienda.usuarios.values()]


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: str):
    usuario = tienda.usuarios.get(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return usuario_a_read(usuario)


# -- productos --
@app.post("/productos", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCreate):
    # según el tipo, pasamos al servicio los datos extra que necesita
    extras = {}
    if datos.tipo == "electronico":
        extras = {"meses_garantia": datos.meses_garantia}
    elif datos.tipo == "ropa":
        extras = {"talla": datos.talla, "color": datos.color}
    producto = tienda.anadir_producto(
        datos.tipo, datos.nombre, datos.precio, datos.stock, **extras
    )
    if producto is None:
        raise HTTPException(status_code=400, detail="tipo de producto no valido")
    return producto_a_read(producto)


@app.get("/productos", response_model=List[ProductoRead])
def listar_productos():
    return [producto_a_read(p) for p in tienda.listar_productos()]


@app.get("/productos/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: str):
    producto = tienda.productos.get(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="producto no encontrado")
    return producto_a_read(producto)


@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: str):
    if not tienda.eliminar_producto(producto_id):
        raise HTTPException(status_code=404, detail="producto no encontrado")
    return {"message": "producto eliminado correctamente"}


# -- pedidos --
@app.post("/pedidos", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def crear_pedido(datos: PedidoCreate):
    # 1. el cliente tiene que existir y ser cliente (un admin no puede comprar)
    usuario = tienda.usuarios.get(datos.cliente_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="cliente no encontrado")
    if not isinstance(usuario, Cliente):
        raise HTTPException(status_code=400, detail="el usuario no es un cliente")

    # 2. si un producto sale repetido, sumamos las cantidades
    solicitados: Dict[str, int] = {}
    for item in datos.items:
        solicitados[item.producto_id] = solicitados.get(item.producto_id, 0) + item.cantidad

    # 3. comprobamos que cada producto existe y que hay stock
    for producto_id, cantidad in solicitados.items():
        producto = tienda.productos.get(producto_id)
        if producto is None:
            raise HTTPException(status_code=404, detail=f"producto {producto_id} no encontrado")
        if not producto.hay_stock(cantidad):
            raise HTTPException(
                status_code=409,
                detail=f"stock insuficiente de '{producto.nombre}' "
                       f"(disponible: {producto.stock}, solicitado: {cantidad})",
            )

    # 4. el servicio descuenta el stock y calcula el total
    pedido = tienda.realizar_pedido(datos.cliente_id, solicitados)
    if pedido is None:
        raise HTTPException(status_code=400, detail="no se pudo crear el pedido")
    return pedido_a_read(pedido)


@app.get("/usuarios/{cliente_id}/pedidos", response_model=List[PedidoRead])
def listar_pedidos_cliente(cliente_id: str):
    if cliente_id not in tienda.usuarios:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return [pedido_a_read(p) for p in tienda.listar_pedidos_usuario(cliente_id)]
