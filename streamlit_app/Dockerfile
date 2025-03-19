# Dockerfile
FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements-hw.txt

# Exponer el puerto donde correrá Streamlit
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
