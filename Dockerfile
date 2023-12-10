FROM python:3.9.13-alpine3.14 as builder

RUN apk -U add build-base unixodbc-dev linux-headers

WORKDIR /usr/lib64

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install wheel

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5080"]