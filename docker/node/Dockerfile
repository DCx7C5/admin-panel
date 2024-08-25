FROM node:latest AS build

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      libssl-dev \
      build-essential && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    npm install -g npm && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

ENV TERM=xterm-256color

RUN groupadd user && usermod -a -G user node

FROM node:latest AS final

WORKDIR /project

COPY --chmod=740 --chown=1000:1000 docker/node/entrypoint.sh /entrypoint.sh
COPY --from=build /etc/passwd /etc/passwd
COPY --from=build /etc/shadow /etc/shadow
COPY --from=build /etc/ssl/certs /etc/ssl/certs
COPY --from=build /etc/ca-certificates /etc/ca-certificates

USER node:1000:1000

ENTRYPOINT ["/entrypoint.sh"]
CMD bash -c "npx webpack --config webpack.config.js --mode development --watch"
