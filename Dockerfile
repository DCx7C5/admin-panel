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

COPY requirements.txt /requirements.txt

RUN pip install --upgrade --no-cache-dir pip
RUN pip install --no-deps --no-cache-dir -r /requirements.txt && \
    rm /requirements.txt && \
    rm -rf /root/.cache

WORKDIR /project

ENTRYPOINT ["/entrypoint.sh"]
