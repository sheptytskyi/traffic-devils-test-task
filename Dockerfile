FROM python:3.11-slim-buster

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /traffic_devils

RUN apt-get update && \
    apt-get install -y \
    python3-dev libpq-dev gcc


COPY requirements.txt /traffic_devils/
RUN pip install -r requirements.txt

EXPOSE 8080

COPY . /traffic_devils