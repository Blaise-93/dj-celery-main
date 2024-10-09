FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install --no-install-recommends -y \
# dependencies for building Python packages
build-essential \
# psycopg2 dependencies
libpq-dev \
pip install -r requirements.txt

COPY ./requirements.txt .


CMD [ "daphne", '-b', '0.0.0.0', '-p', '8001', 'dj_celery.asgi:application' ]


