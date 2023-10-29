LABEL org.opencontainers.image.description "Removes client files compressions to fix plank page on safari"

FROM ubuntu:latest

WORKDIR /

COPY ./dist/swingmusic /swingmusic

RUN chmod +x /swingmusic

EXPOSE 1970/tcp

VOLUME /music

VOLUME /config

ENTRYPOINT ["/swingmusic", "--host", "0.0.0.0", "--config", "/config"]
