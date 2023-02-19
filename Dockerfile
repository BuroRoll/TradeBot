FROM python:3.10

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./src ./
COPY requirements.txt requirements.txt
COPY .env .env

RUN pip install -r requirements.txt
CMD ["python", "."]