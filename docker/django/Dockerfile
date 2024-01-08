FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get -y --no-install-recommends install wget gnupg && \
    echo "deb https://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" | tee -a '/etc/apt/sources.list.d/pgdg.list' && \
    wget --quiet -O - "https://www.postgresql.org/media/keys/ACCC4CF8.asc" | apt-key add -

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
      postgresql-client-16 \
      python3-dev \
      gcc \
      build-essential  \
      wget \
      libpq-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

RUN useradd -U -m -l -s /bin/bash -u 1000 user && usermod -aG sudo user

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TERM xterm-256color

WORKDIR /project

COPY ./docker/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown 1000:1000 /entrypoint.sh

USER user:1000:1000

ENTRYPOINT ["/entrypoint.sh"]
