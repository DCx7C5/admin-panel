FROM node:latest

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
      libssl-dev \
      build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    npm install -g npm && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

ENV TERM xterm-256color

RUN groupadd user && usermod -a -G user node

WORKDIR /project

COPY ./docker/node/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown 1000:1000 /entrypoint.sh

USER node:1000:1000

ENTRYPOINT ["/entrypoint.sh"]
