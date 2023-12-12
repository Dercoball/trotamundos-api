FROM python:3.9.13-alpine3.14 as builder

RUN apk --no-cache add unixODBC unixODBC-dev

RUN apk --no-cache add build-base unixodbc-dev linux-headers

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install wheel

COPY . .

RUN apk --no-cache add --virtual .build-deps curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
RUN install -o root -g root -m 644 microsoft.gpg /etc/apk/keys/
RUN echo "https://packages.microsoft.com/alpine/3.14/prod" > /etc/apk/repositories
RUN apk --no-cache add msodbcsql17
RUN apk del .build-deps

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5080"]