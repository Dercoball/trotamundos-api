FROM python:3.11.1

WORKDIR /code

# Copia los archivos necesarios
COPY ./ /code/

# Instalar las dependencias necesarias para wkhtmltopdf
RUN apt-get update \
    && apt-get install -y \
    wget \
    ca-certificates \
    fontconfig \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    libssl-dev \
    && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1/wkhtmltox_0.12.6.1-1.bionic_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6.1-1.bionic_amd64.deb \
    && apt-get install -f -y \
    && rm wkhtmltox_0.12.6.1-1.bionic_amd64.deb  # Limpieza de archivos temporales

# Instala el controlador ODBC para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Instala las dependencias de Python
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# CMD para ejecutar tu aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5080"]
