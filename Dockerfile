FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-client \
    postgresql-dev

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY .env /.env
COPY requirements.txt /requirements.txt

RUN chmod 600 /.env

RUN pip install --upgrade pip
RUN pip install --no-deps -r /requirements.txt && \
    rm /requirements.txt && \
    rm -rf /root/.cache

WORKDIR /project

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]