FROM python:3.9.13-alpine3.14 as builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        unixodbc \
        unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*
    
ENV ACCEPT_EULA=Y
ENV ODBC_VERSION=17
ENV ODBC_DRIVER=ODBC\ Driver\ $ODBC_VERSION\ for\ SQL\ Server

# Instala el controlador ODBC de SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        $ODBC_DRIVER \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install wheel

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5080"]