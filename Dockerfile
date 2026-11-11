# imagen de la api de la tienda el cowboy espacial (fastapi + uvicorn)
FROM python:3.12-slim

# no generar ficheros .pyc y mostrar los logs al momento
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# primero solo las dependencias, para aprovechar la caché de docker:
# si no cambia requirements.txt, esta capa no se vuelve a construir
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# código fuente de la api
COPY src/ ./src/

# usuario sin privilegios: la app no se ejecuta como root
RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /app
USER appuser

WORKDIR /app/src
EXPOSE 8000

# arranque de la api (el puerto se puede cambiar con la variable PORT)
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
