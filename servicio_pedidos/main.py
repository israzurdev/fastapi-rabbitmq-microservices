from fastapi import FastAPI
from pydantic import BaseModel
import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Microservicio Pedidos")

#Configuracion Rabbit / user, pass y host
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")
RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")

#Esquema de datos

class Pedido(BaseModel):
    producto: str
    cantidad: int
    email_cliente: str
    
@app.post("/pedidos")
async def crear_pedido(pedido: Pedido):
    #Conectamos con el Broker RabbitMQ
    credenciales = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    conexion = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, credentials=credenciales))
    canal = conexion.channel()
    
    #Declaramos si existe o no la cola. Si no, la creamos (Idempotencia)
    canal.queue_declare(queue='cola_notificaciones')
    #Conversión del objeto Pedido a JSON para que viaje por la red
    mensaje = json.dumps(pedido.model_dump())
    #Mensaje en cola
    canal.basic_publish(
        exchange='',
        routing_key='cola_notificaciones',
        body=mensaje
    )
    #Cerramos la conexion
    conexion.close()
    #Respuesta. Procesamiento en otro servicio de forma asíncrona
    return {
        "status": "ok",
        "mensaje": "Pedido recibido. Encolado correctamente."
    }