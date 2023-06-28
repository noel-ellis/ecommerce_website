# syntax = docker/dockerfile:1.2

FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/ecomm
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000