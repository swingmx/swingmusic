FROM ubuntu:latest

WORKDIR /

COPY ./dist/swingmusic /swingmusic

RUN chmod +x /swingmusic

EXPOSE 1970/tcp

VOLUME /music

VOLUME /config

ENTRYPOINT ["/swingmusic", "--host", "0.0.0.0", "--config", "/config"]

LABEL org.opencontainers.image.source=https://github.com/cwilvx/swingmusic
LABEL org.opencontainers.image.description=" Swing Music is a beautiful, self-hosted music player for your local audio files. Like a cooler Spotify ... but bring your own music."
LABEL org.opencontainers.image.licenses=MIT