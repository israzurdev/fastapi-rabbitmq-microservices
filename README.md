#  Arquitectura de Microservicios con FastAPI y RabbitMQ

¡Hola! 👋 Bienvenido a este pequeño (pero matón) proyecto de arquitectura asíncrona. 

Lo he desarrollado como un reto personal para profundizar en el mundo de los microservicios, la mensajería asíncrona y la orquestación de contenedores. Actualmente lo tengo corriendo de forma nativa en una Raspberry Pi en mi red local.

##  ¿De qué va esto?

El objetivo era simular el backend de un e-commerce donde no queremos que el usuario se quede esperando mirando una pantalla de carga mientras nosotros procesamos cosas pesadas por detrás (como enviar emails, generar PDFs o validar pagos).

Para solucionarlo, he montado un sistema de **Productores y Consumidores** usando RabbitMQ como intermediario:

1. **La API (FastAPI):** Recibe el pedido del cliente, lo empaqueta rápido, se lo tira a RabbitMQ y le dice al cliente: *"Todo OK, ya nos encargamos"*. (Tiempo de respuesta: milisegundos).
2. **El Broker (RabbitMQ):** Guarda el mensaje en una cola de forma segura.
3. **El Worker (Python):** Un trabajador incansable que está suscrito a la cola. Coge el pedido, hace el trabajo pesado simulado (en este caso un retardo artificial y mandar un email falso) y confirma que ha terminado para coger el siguiente.

## 🛠️ Stack Tecnológico

* **FastAPI:** Para el endpoint del productor. Rápido y moderno.
* **RabbitMQ:** Como broker de mensajería (AMQP).
* **Pika:** La librería de Python para hablar con RabbitMQ.
* **Docker & Docker Compose:** Para orquestar toda la infraestructura y evitar el clásico "en mi máquina funciona".

## 🚀 Cómo levantarlo en tu máquina

Si quieres trastear con él, es súper fácil. Solo necesitas tener Docker instalado:

1. Clona este repositorio.
2. Crea un archivo llamado `.env` en la raíz copiando la estructura de `.env.example` y pon tus propias contraseñas.
3. Levanta la orquesta ejecutando en la terminal: `docker-compose up --build -d`
4. Visita `http://localhost:8000/docs` para lanzar peticiones desde Swagger.
5. Visita `http://localhost:15672` para ver el panel de control de RabbitMQ.

## 🧠 Aprendizajes por el camino
Pelearme con las redes internas de Docker, lidiar con los volúmenes persistentes y manejar la salida estándar de Python en contenedores para ver los logs en tiempo real han sido algunos de los mayores retos (¡y victorias!) de este proyecto.