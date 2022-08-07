FROM python:3.10.5-alpine3.15

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./ ./
RUN pip install -r requirements.txt