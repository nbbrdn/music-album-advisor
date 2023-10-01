FROM python:3.10-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install psycopg2-binary

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app/