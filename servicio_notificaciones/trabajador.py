import pika
import json
import time
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")
RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")

def procesar_notificacion(ch, method, properties, body):
    print("\n[x] Nuevo evento en la cola...")
    pedido = json.loads(body)
    
    print(f"Enviando email de confirmacion a: {pedido['email_cliente']}")
    print(f"Tramitando el producto: {pedido['producto']} (Cantidad: {pedido['cantidad']})")
    
    # Simulamos un proceso pesado de 3 segundos
    time.sleep(3) 
    
    print("[x] Email enviado con éxito.")
    # Confirmamos a RabbitMQ que ya puede borrar el mensaje
    ch.basic_ack(delivery_tag=method.delivery_tag)

def iniciar_trabajador():
    credenciales = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    conexion = None
    
    # Bucle de reintentos: 12 intentos (1 minuto) para que RabbitMQ arranque
    for intento in range(12):
        try:
            print(f"[*] Intentando conectar a RabbitMQ en {RABBIT_HOST} (Intento {intento + 1}/12)...")
            conexion = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, credentials=credenciales))
            print("[*] ¡Conexión establecida con éxito!")
            break
        except pika.exceptions.AMQPConnectionError:
            print("[!] RabbitMQ aún no está listo. Esperando 5 segundos...")
            time.sleep(5)
            
    if not conexion:
        print("[X] Imposible conectar al Broker. Apagando trabajador.")
        return

    canal = conexion.channel()
    canal.queue_declare(queue='cola_notificaciones')
    canal.basic_qos(prefetch_count=1)
    canal.basic_consume(queue='cola_notificaciones', on_message_callback=procesar_notificacion)

    print('[*] El Servicio de Notificaciones está activo y escuchando...')
    canal.start_consuming()

if __name__ == "__main__":
    iniciar_trabajador()