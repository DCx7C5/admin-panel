FROM redis:alpine3.19

RUN apk update &&  \
    apk add  \
    --no-interactive \
    --no-cache \
      libressl-dev \
      alpine-sdk && \
    apk -v cache clean

ENV TERM xterm-256color

COPY ./docker/redis/redis.conf /etc/redis.conf
RUN chown 1000:1000 /etc/redis.conf
RUN mkdir -p /tmp/redis/ &&  \
    chmod 777 -R /tmp/redis &&  \
    chown -R 1000:1000 /tmp/redis/

USER redis:1000:1000