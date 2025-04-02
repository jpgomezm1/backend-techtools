FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Puerto que Flask utilizará
EXPOSE 8080

# Variable para asegurar que Flask use el puerto correcto
ENV PORT=8080

# Usar gunicorn como servidor WSGI
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 run:app