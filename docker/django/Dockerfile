FROM debian:12-slim

RUN apt update && apt-get install --no-install-recommends -y \
      build-essential \
      wget \
      gnupg \
      gcc \
      sudo \
      python3-dev \
      python3-pip \
      python3-wheel \
      libpq-dev \
      redis-tools \
      postgresql-client && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

RUN ln -s /usr/bin/python3.11 /usr/bin/python
RUN useradd -U -m -l -s /bin/bash -u 1000 django && usermod -aG sudo django

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm-256color
COPY --chmod=740 --chown=1000:1000 docker/django/entrypoint.sh /entrypoint.sh

WORKDIR /project

COPY ../../requirements.txt /project/requirements.txt

RUN python -m pip install --no-cache-dir --break-system-packages -U pip && \
    python -m pip install --no-cache-dir --break-system-packages -r /project/requirements.txt

USER django:1000:1000

ENTRYPOINT ["/entrypoint.sh"]
CMD /bin/bash