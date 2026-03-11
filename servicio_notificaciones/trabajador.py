import pika
import json
import time
import os
from dotenv import load_dotenv

#Credenciales de RabbitMQ
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")
RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")

#Función que se ejecuta cada vez que llega un mensaje
def procesar_notificacion(ch, method, properties, body):
    print("\n [x] Nuevo evento en la cola...")
    
    #De JSON a diccionario en python
    pedido = json.loads(body)
    
    #Simulacion de proceso pesado
    print(f"Enviando email de confirmacion a : {pedido['email_cliente']}")
    print(f"Tramitando el producto: {pedido['producto']} (Cantidad: {pedido['cantidad']})")
    
    time.sleep(3) #Pausa 3s [procesando]
    
    print("[x] Email enviado con éxito.")
    #Confirmacion a RabbitMQ para que borre el mensaje
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
def iniciar_trabajador():
    #Abrir conexion
    credenciales = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    conexion = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, credentials=credenciales))
    canal = conexion.channel()
    #Aseguramos que existe la cola
    canal.queue_declare(queue='cola_notificaciones')
    
    #No saturamos RAM, enviamos solo un mensaje
    canal.basic_qos(prefetch_count=1)
    
    #Configuracion de quien procesa los mensajes
    canal.basic_consume(queue='cola_notificaciones', on_message_callback=procesar_notificacion)
    
    print("[*] El Servicio de Notificaciones está activo y escuchando... (Ctrl + C para salir)")
    
    #Bucle infinito
    canal.start_consuming()

if __name__ == '__main__':
    iniciar_trabajador()