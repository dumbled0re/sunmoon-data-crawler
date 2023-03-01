FROM --platform=linux/x86_64 python:3.11.1-bullseye

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y unzip

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r ./requirements.txt

COPY ./app ./
