FROM python:3.9-slim 

WORKDIR /opt/star-burger
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .

RUN apt update
RUN apt install -y python3-pip libpq-dev
RUN apt-get install -y python3-dev postgresql postgresql-contrib
RUN pip3 install -r requirements.txt

COPY . .
