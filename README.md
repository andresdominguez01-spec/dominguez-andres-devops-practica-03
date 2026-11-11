el cowboy espacial - api de tienda online

autor: andrés domínguez garcía

asignatura: arquitectura del software - uie

descripción

api rest desarrollada en python con fastapi para gestionar una tienda online ("el cowboy espacial"). permite:

- usuarios: crear y consultar clientes y administradores.
- productos: crear, listar, consultar y eliminar productos (normales, electrónicos con garantía y ropa con talla y color).
- pedidos: crear pedidos para un cliente (con control de stock) y consultar el historial de pedidos de cada usuario.

los datos se guardan en memoria y la api arranca con unos datos de ejemplo cargados para poder probarla desde el primer momento.

el proyecto incluye además:

- `cliente_python/cliente.py`: cliente en python (requests) que recorre todo el flujo de la api.
- `frontend/index.html`: frontend sencillo en html y javascript que consume la api.

estructura del proyecto

```
.
├── src/                    # código de la api
│   ├── main.py             # endpoints de fastapi
│   ├── schemas.py          # esquemas pydantic (validación de entrada y salida)
│   ├── models/             # clases usuario, producto y pedido
│   └── services/           # tiendaservice: lógica de la tienda
├── cliente_python/         # cliente de prueba en python
├── frontend/               # frontend html
└── requirements.txt        # dependencias
```

ejecución en local (sin docker)

```bash
pip install -r requirements.txt
cd src
python -m uvicorn main:app --reload
```

- documentación interactiva: http://localhost:8000/docs
- cliente de prueba (con la api encendida, en otra terminal): `python cliente_python/cliente.py`
- frontend: abrir `frontend/index.html` en el navegador.
