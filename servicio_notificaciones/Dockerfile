FROM python:3.10-slim

WORKDIR /app

#Copiamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copiamos el codigo de trabajado
COPY servicio_notificaciones/ .

#Comando para arrancar
CMD ["python", "trabajador.py"]