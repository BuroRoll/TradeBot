FROM python:3.9-alpine

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./ ./
RUN apt-get -y install libc-dev
RUN apt-get -y install build-essential
RUN pip install -U pip

RUN pip install -r requirements.txt
CMD [ "python", "./main.py"]