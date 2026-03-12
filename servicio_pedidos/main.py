from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import pika
import json
import os
from dotenv import load_dotenv, find_dotenv

#Cargamos las variables
load_dotenv(find_dotenv())

#Credenciales de RabbitMQ
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")
RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")

#Configuración de seguridad 
API_KEY_NAME = "X-Api-Key"
API_KEY_SECRETA = os.getenv("API_SECRET_KEY", "clave_por_defecto_insegura")

#Le decimos a FastAPI que busque la clave en las cabeceras (Headers) de la petición
api_key_header =  APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verificar_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY_SECRETA:
        return api_key
    #Si no coincide o no existe, lanza error 403(Forbidden)
    raise HTTPException(status_code=403, detail="Acceso denegado: API Key inválida o ausente.")

app = FastAPI(title="API de Pedidos")

class Pedido(BaseModel):
    producto: str
    cantidad: int
    email_cliente: str
    
#Ahora pasamos 'api_key: str = (verificar_api_key)' al endpoint
@app.post("/pedidos")
async def crear_pedido(pedido: Pedido, api_key: str = Depends(verificar_api_key)):
    credenciales = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    conexion = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, credentials=credenciales))
    canal = conexion.channel()
    
    canal.queue_declare(queue='cola_notificaciones')
    
    mensaje = json.dumps(pedido.model_dump())
    canal.basic_publish(
        exchange='',
        routing_key='cola_notificaciones',
        body=mensaje
    )
    conexion.close()
    return{"status": "ok", "mensaje": "Pedido recibido y validado. Encolado correctamente."}