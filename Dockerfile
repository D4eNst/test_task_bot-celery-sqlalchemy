# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /app
COPY . .

RUN useradd -ms /bin/bash celeryuser
USER celeryuser
CMD python3 -m src & \
    celery -A task.celery_worker:app worker --loglevel=warning & \
    celery -A task.celery_worker:app beat --loglevel=warning