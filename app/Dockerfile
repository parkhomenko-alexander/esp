FROM python:3.9-alpine

WORKDIR /app
ADD . /app
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD gunicorn --bind 0.0.0.0:5000 main:app
