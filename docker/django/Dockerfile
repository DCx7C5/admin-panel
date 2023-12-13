FROM python:slim-bookworm

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
      postgresql-client  \
      python3-dev \
      gcc \
      build-essential \
      libpq-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

RUN useradd -U -m -l -s /bin/bash -u 1000 user

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TERM xterm-256color

WORKDIR /project

COPY ./docker/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown 1000:1000 /entrypoint.sh

USER user:1000:1000

ENTRYPOINT ["/entrypoint.sh"]
