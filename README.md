# 🚀 Arquitectura de Microservicios: FastAPI + RabbitMQ (EDA)


![test](https://github.com/user-attachments/assets/6b86e198-cbb6-4f39-8c86-89ea7a771685)



¡Buenas! 👋 Bienvenido a este proyecto montado como prueba de concepto (PoC) para trastear con una **Arquitectura Orientada a Eventos (EDA)**. 

Lo he desarrollado como un reto personal para profundizar en el mundo de los microservicios, la mensajería asíncrona y la orquestación de contenedores. Actualmente lo tengo corriendo de forma nativa en una Raspberry Pi en mi red local.

## 💡 ¿El problema a resolver?

La idea principal era resolver un problema clásico de Backend: ¿qué pasa cuando tu API tiene que hacer algo que tarda mucho (como mandar un email, generar un PDF o procesar un pago) y no quieres dejar al usuario mirando una pantalla de carga eterna? La solución: desacoplar procesos usando un Message Broker.

## 🧠 Cómo funciona la magia

He montado un sistema de **Productores y Consumidores** usando RabbitMQ como intermediario:

1. **El Cliente** le pega al endpoint `/pedidos` mediante un simple `POST`.
2. **La API (FastAPI - Productor):** Recibe el pedido, lo valida volando con Pydantic, lo empaqueta y se lo tira a la cola de RabbitMQ. Inmediatamente devuelve un `200 OK` ("Todo OK, ya nos encargamos"). Cero esperas para el usuario.
3. **El Broker (RabbitMQ):** Es el guardián. Se guarda el evento a salvo. Si el resto del sistema se cae, el mensaje sigue ahí esperándonos. Cero pérdida de datos.
4. **El Worker (Python - Consumidor):** Un trabajador incansable en segundo plano suscrito a la cola. Pilla el evento, hace el trabajo sucio simulado (un retardo artificial y mandar un email falso) y confirma a RabbitMQ que ha terminado para coger el siguiente.

## 🛠️ Stack Tecnológico

* **Backend API:** Python 3, FastAPI, Pydantic, Uvicorn.
* **Message Broker:** RabbitMQ (AMQP).
* **Integración:** Pika (Librería de Python para hablar con RabbitMQ).
* **Orquestación:** Docker & Docker Compose (para evitar el clásico "en mi máquina funciona").

## 🚀 Cómo levantarlo en tu máquina

Si quieres trastear con él, es súper fácil. Solo necesitas tener Docker instalado:

1. Clona este repositorio:
    git clone https://github.com/israzurdev/fastapi-rabbitmq-microservices.git
    cd fastapi-rabbitmq-microservices

2. Crea un archivo llamado `.env` en la raíz copiando la estructura de `.env.example` y pon tus propias contraseñas.

3. Levanta la orquesta ejecutando en la terminal: 
    docker-compose up --build -d

4. Visita `http://localhost:8000/docs` para lanzar peticiones desde Swagger.

5. Visita `http://localhost:15672` para ver el panel de control de RabbitMQ.

## 🗺️ Roadmap y Estado del Proyecto

Esto empezó como un MVP, pero el proyecto está vivo y escalando:

- [x] **Fase 1:** MVP funcionando. FastAPI hablando con RabbitMQ.
- [x] **Fase 2:** Orquestar todo de golpe con un `docker-compose` y variables de entorno seguras.
- [ ] **Fase 3:** Securizar el endpoint público con una API Key (mitigando riesgos OWASP A01).
- [ ] **Fase 4:** Conectarle una base de datos real (SQLite/PostgreSQL) con SQLAlchemy para darle persistencia a los pedidos.

---
*Escrito a base de teclado y café por Israel - SysAdmin & Backend Developer.*
