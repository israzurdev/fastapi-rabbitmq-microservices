#  Microservicios Asíncronos (FastAPI + RabbitMQ)

¡Buenas! He montado este proyecto como prueba de concepto (PoC) para trastear con una **Arquitectura Orientada a Eventos (EDA)**. 

La idea principal era resolver un problema clásico de Backend: ¿qué pasa cuando tu API tiene que hacer algo que tarda mucho (como mandar un email, generar un PDF o procesar un pago) y no quieres dejar al usuario mirando una pantalla de carga eterna? La solución: desacoplar procesos usando un Message Broker.

## 🧠 Cómo funciona la magia

1. **El Cliente** le pega al endpoint `/pedidos` mediante un simple `POST`.
2. **La API (El Productor)** coge el pedido, lo valida volando con Pydantic, y lo lanza a una cola de RabbitMQ. Inmediatamente te devuelve un `200 OK`. Cero esperas para el usuario.
3. **RabbitMQ (El Broker)** es el guardián. Se guarda el evento a salvo. Si el resto del sistema se cae, el mensaje sigue ahí esperándonos. Cero pérdida de datos.
4. **El Trabajador (El Consumidor)** es un script en segundo plano que está siempre escuchando. Pilla el evento de la cola, hace el trabajo sucio simulado y confirma que ha terminado.

## 🛠️ Con qué lo he montado

* **Backend API:** Python 3, FastAPI, Pydantic, Uvicorn
* **Message Broker:** RabbitMQ (corriendo aislado en Docker)
* **Librería AMQP:** Pika
* **Gestión de Entorno:** python-dotenv

## Cómo levantarlo en tu máquina (Fase 1)

Si quieres trastear con el código, asegúrate de tener Python 3.10+ y Docker a mano.

**1. Clona y prepara la burbuja (entorno virtual):**
```bash
git clone https://github.com/israzurdev/fastapi-rabbitmq-microservices.git
cd fastapi-rabbitmq-microservices
python -m venv venv
source venv/bin/activate  # Si estás en Windows usa: .\venv\Scripts\activate
pip install -r requirements.txt
```

**2. Las variables de entorno:**
Tienes un archivo `.env.example`. Cópialo y renómbralo a `.env`. Por defecto usa `guest/guest` para levantar el RabbitMQ en local.
```bash
cp .env.example .env
```

**3. Despierta al Broker:**
```bash
docker run -d --hostname mi-rabbit --name broker-mensajes -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

**4. Levanta la API:**
```bash
cd servicio_pedidos
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
*(Échale un ojo a la documentación interactiva que se genera sola en `http://localhost:8000/docs`)*

**5. Pon a currar al trabajador:**
En una terminal nueva (asegurate de estar usando el entorno virtual), lanza:
```bash
cd servicio_notificaciones
python trabajador.py
```

## 🗺️ Lo que se viene (Roadmap)

Esto es solo el MVP inicial, pero el proyecto está vivo. Esto es lo próximo que le voy a meter a la arquitectura:

- [x] **Fase 1:** MVP funcionando. FastAPI hablando con RabbitMQ.
- [ ] **Fase 2:** Orquestar todo de golpe con un `docker-compose` y securizar el endpoint público con una API Key (mitigando riesgos OWASP A01).
- [ ] **Fase 3:** Conectarle una base de datos real (SQLite/PostgreSQL) con SQLAlchemy para darle persistencia a los pedidos.

---
*Escrito a base de teclado y café por Israel - SysAdmin & Backend Developer.*
