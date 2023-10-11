FROM ubuntu:latest

WORKDIR /

COPY ./dist/swingmusic /swingmusic

EXPOSE 1970/tcp

VOLUME /music

VOLUME /config

ENTRYPOINT ["/swingmusic", "--host", "0.0.0.0", "--config", "/config"]
