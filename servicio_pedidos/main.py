from fastapi import FastAPI
from pydantic import BaseModel
import pika
import json
import os
from dotenv import load_dotenv, find_dotenv

# Cargamos las variables de entorno
load_dotenv(find_dotenv())

# Credenciales seguras (si no hay .env, usa "guest" por defecto para no exponer claves)
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")
RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")

app = FastAPI(title="API de Pedidos")

class Pedido(BaseModel):
    producto: str
    cantidad: int
    email_cliente: str

@app.post("/pedidos")
async def crear_pedido(pedido: Pedido):
    # Conectamos con el Broker RabbitMQ
    credenciales = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    conexion = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, credentials=credenciales))
    canal = conexion.channel()

    # Aseguramos que la cola existe
    canal.queue_declare(queue='cola_notificaciones')
    
    # Preparamos el mensaje
    mensaje = json.dumps(pedido.model_dump())
    
    # Publicamos el mensaje en la cola
    canal.basic_publish(
        exchange='',
        routing_key='cola_notificaciones',
        body=mensaje
    )
    
    conexion.close()
    return {"status": "ok", "mensaje": "Pedido encolado correctamente y listo para procesar"}