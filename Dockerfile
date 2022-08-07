FROM python:3.9-alpine

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./ ./
RUN apk add --update make cmake gcc g++ gfortran
RUN apk add --update python py-pip python-dev
RUN pip install -r requirements.txt
CMD [ "python", "./main.py"]