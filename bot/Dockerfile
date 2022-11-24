FROM python:3.10-slim-buster

WORKDIR /usr/src/advisor

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt /usr/src/advisor/requirements.txt
RUN pip install -r requirements.txt

COPY /app /usr/src/advisor/
COPY main.py /usr/src/advisor/
