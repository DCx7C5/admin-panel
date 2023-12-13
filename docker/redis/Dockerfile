FROM redis:bookworm

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
      libssl-dev \
      build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

ENV TERM xterm-256color

RUN groupadd user && usermod -a -G user redis

WORKDIR /project

COPY ./docker/redis/redis.conf /etc/redis.conf
RUN chown 999:1000 /etc/redis.conf
RUN mkdir -p /tmp/redis && chown -R 999:1000 /tmp/redis

USER redis:999:1000
