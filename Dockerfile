FROM python:3.9-alpine

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./ ./
#RUN apk add --no-cache --update \
#    python3 python3-dev gcc \
#    gfortran musl-dev \
#    libffi-dev openssl-dev
RUN pip install -r requirements.txt
CMD [ "python", "./main.py"]