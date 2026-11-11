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

docker

la api está contenerizada con docker. la imagen se basa en python:3.12-slim, instala las dependencias de requirements.txt (con versiones fijadas), copia el código de src/ y se ejecuta con un usuario sin privilegios (appuser). el fichero .dockerignore evita copiar a la imagen lo que no hace falta (.git, entornos virtuales, cachés de python, el cliente y el frontend).

imagen publicada en docker hub: https://hub.docker.com/r/andresdominguezuie/tienda-api

construir la imagen (desde la raíz del repositorio)

```bash
docker build -t tienda-api:1.0 .
```

ejecutar el contenedor

```bash
# en segundo plano, publicando el puerto 8000
docker run -d -p 8000:8000 --name tienda-api tienda-api:1.0

# ver que está en marcha y consultar los logs
docker ps
docker logs tienda-api

# usando otro puerto dentro del contenedor (variable PORT)
docker run -d -p 9000:9000 -e PORT=9000 --name tienda-api-9000 tienda-api:1.0

# parar y borrar el contenedor
docker stop tienda-api
docker rm tienda-api
```

descargar y ejecutar la imagen desde docker hub (sin construirla)

```bash
docker pull andresdominguezuie/tienda-api:1.0
docker run -d -p 8000:8000 --name tienda-api andresdominguezuie/tienda-api:1.0
```

publicar la imagen en docker hub

```bash
docker login
docker tag tienda-api:1.0 andresdominguezuie/tienda-api:1.0
docker tag tienda-api:1.0 andresdominguezuie/tienda-api:latest
docker push andresdominguezuie/tienda-api:1.0
docker push andresdominguezuie/tienda-api:latest
```

variables de entorno

- `PORT`: puerto en el que escucha la api dentro del contenedor (por defecto 8000).
- `API_URL` (solo para el cliente de python): dirección de la api (por defecto http://localhost:8000).

la api no usa secretos ni claves, así que no hace falta ningún fichero .env.

pruebas y salida esperada

con el contenedor en marcha:

1. al hacer `docker logs tienda-api` debe aparecer `Uvicorn running on http://0.0.0.0:8000`.
2. en http://localhost:8000/docs se ve la documentación interactiva con todos los endpoints (usuarios, productos y pedidos).
3. en http://localhost:8000/productos se devuelve en json la lista de productos de ejemplo.
4. el cliente recorre todo el flujo de la api (crear usuario, crear productos, crear pedido, consultar pedidos y comprobar un error 409 por falta de stock):

```bash
pip install requests
python cliente_python/cliente.py
```

y debe terminar con:

```
Flujo completado correctamente.
```
