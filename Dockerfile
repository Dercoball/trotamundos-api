FROM python:3.9.13-alpine3.14 as builder

RUN apk -U add build-base unixodbc-dev linux-headers
RUN apk add python3 python3-dev g++ unixodbc-dev
# Copia el controlador ODBC para SQL Server al contenedor
COPY ./odbc-driver /odbc-driver

# Agrega la ruta del controlador al LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/odbc-driver:$LD_LIBRARY_PATH

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install wheel

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5080"]