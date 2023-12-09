FROM python:3.9.13-alpine3.14 as builder

RUN apk -U add build-base unixodbc-dev linux-headers

WORKDIR /usr/src/app

COPY requirements.txt .

ADD odbcinst.ini /etc/odbcinst.ini
RUN apt-get update
RUN apt-get install -y tdsodbc unixodbc-dev
RUN apt install unixodbc-bin -y
RUN apt-get clean -y

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install wheel

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5080"]