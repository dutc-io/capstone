FROM python:3.11.1-buster

COPY ./backend /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
