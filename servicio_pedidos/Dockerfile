FROM python:3.10-slim

WORKDIR /app

#Copiamos dependencias y las instalamos

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copiamos el codigo de la API

COPY servicio_pedidos/ .

#Exponemos el puerto de FastAPI
EXPOSE 8000

#Arrancamos el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]