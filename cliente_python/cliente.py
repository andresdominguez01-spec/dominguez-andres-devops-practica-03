# cliente de python (requests) para la api de la tienda.
# va aparte del servidor: no importa nada suyo, todo se hace por http.
#
# uso:
#   python cliente.py                                  -> api en localhost
#   python cliente.py --url http://192.168.1.34:8000   -> api en otro equipo
#   (también vale la variable de entorno API_URL)
import argparse
import os
import sys
import time

import requests

# dirección base de la api: se cambia aquí, con --url o con la variable API_URL
BASE_URL = os.environ.get("API_URL", "http://localhost:8000")


def peticion(metodo: str, ruta: str, esperado: int, **kwargs):
    # hace la petición, comprueba el código http y devuelve el json
    # esperado = el código que damos por bueno (200, 201...)
    # si no coincide, lanza un error con el detalle que manda el servidor
    url = f"{BASE_URL}{ruta}"
    respuesta = requests.request(metodo, url, timeout=10, **kwargs)
    print(f"  {metodo} {ruta} -> {respuesta.status_code}")
    try:
        datos = respuesta.json()
    except ValueError:
        datos = None
    if respuesta.status_code != esperado:
        detalle = datos.get("detail") if isinstance(datos, dict) else respuesta.text
        raise RuntimeError(f"se esperaba {esperado} y se recibio {respuesta.status_code}: {detalle}")
    return datos


def titulo(texto: str) -> None:
    print(f"\n=== {texto} ===")


def main() -> None:
    sufijo = str(int(time.time()))  # evita emails repetidos al relanzar el script

    titulo("1. Crear un usuario (cliente)")
    cliente = peticion("POST", "/usuarios", 201, json={
        "tipo": "cliente",
        "nombre": "Spike Spiegel",
        "email": f"spike{sufijo}@bebop.com",
        "direccion": "Calle Bebop 5, Vigo",
    })
    print("  creado:", cliente)

    titulo("2. Consultar la lista de usuarios")
    usuarios = peticion("GET", "/usuarios", 200)
    for u in usuarios:
        print(f"  - {u['nombre']} <{u['email']}> admin={u['es_admin']} id={u['id'][:8]}")

    titulo("3. Crear productos")
    productos = [
        {"tipo": "electronico", "nombre": "Reproductor de Blu-ray", "precio": 89.90,
         "stock": 10, "meses_garantia": 24},
        {"tipo": "ropa", "nombre": "Camiseta Cowboy Bebop", "precio": 22.95,
         "stock": 15, "talla": "M", "color": "negro"},
        {"tipo": "normal", "nombre": "Poster de cine", "precio": 9.50, "stock": 30},
    ]
    creados = [peticion("POST", "/productos", 201, json=p) for p in productos]
    for p in creados:
        print(f"  creado: {p['nombre']} ({p['tipo']}) id={p['id'][:8]}")

    titulo("4. Consultar la lista de productos")
    for p in peticion("GET", "/productos", 200):
        print(f"  - {p['nombre']}: {p['precio']}EUR, stock {p['stock']}")

    titulo("5. Crear un pedido para el usuario")
    pedido = peticion("POST", "/pedidos", 201, json={
        "cliente_id": cliente["id"],
        "items": [
            {"producto_id": creados[0]["id"], "cantidad": 1},
            {"producto_id": creados[2]["id"], "cantidad": 2},
        ],
    })
    print(f"  pedido {pedido['id'][:8]} total={pedido['total']}EUR")

    titulo("6. Consultar los pedidos del usuario")
    for p in peticion("GET", f"/usuarios/{cliente['id']}/pedidos", 200):
        print(f"  pedido {p['id'][:8]} - {p['fecha']} - total {p['total']}EUR")
        for it in p["items"]:
            print(f"     {it['cantidad']} x {it['nombre']} = {it['subtotal']}EUR")

    titulo("7. Comprobar un error controlado (stock insuficiente -> 409)")
    try:
        peticion("POST", "/pedidos", 201, json={
            "cliente_id": cliente["id"],
            "items": [{"producto_id": creados[0]["id"], "cantidad": 9999}],
        })
    except RuntimeError as e:
        print("  error esperado:", e)

    print("\nFlujo completado correctamente.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente de la API de la tienda")
    parser.add_argument("--url", default=BASE_URL, help="direccion base de la API")
    BASE_URL = parser.parse_args().url.rstrip("/")
    print(f"Usando API en {BASE_URL}")
    try:
        main()
    except requests.exceptions.ConnectionError:
        sys.exit(f"No se pudo conectar con {BASE_URL}. Esta el servidor en marcha?")
    except (RuntimeError, requests.exceptions.RequestException) as e:
        sys.exit(f"Error: {e}")