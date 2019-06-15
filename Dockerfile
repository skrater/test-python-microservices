FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .

RUN DOCKERIZE_VERSION=v0.6.1 \
	&& apk update \
 	&& apk add postgresql-libs \
 	&& apk add --virtual .build-deps gcc musl-dev postgresql-dev wget \
	&& wget --no-check-certificate https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
	&& tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
 	&& pip install -r requirements.txt --no-cache-dir \
 	&& apk --purge del .build-deps
