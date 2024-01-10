##### CLIENT #####
FROM node:16 as build-client

COPY ./swingmusic-client/ /build

WORKDIR /build
RUN yarn install && yarn build --outDir /out

###### SERVER ######
FROM python:3.10.11 as build-server

COPY . /build
COPY --from=build-client /out /build/client

WORKDIR /build
ENV LASTFM_API_KEY "missing"
ENV PLUGIN_LYRICS_AUTHORITY "missing"
ENV PLUGIN_LYRICS_ROOT_URL "missing"
ENV SWINGMUSIC_APP_VERSION "missing"

RUN apt update && apt install -y ffmpeg && apt autoclean -y && rm -rf /var/lib/apt/lists/*
RUN pip install poetry
RUN python -m poetry install && \
 python -m poetry config virtualenvs.create false && \
 python -m poetry run python manage.py --build

# Release
FROM ubuntu:latest

RUN apt update && apt install -y --no-install-recommends ffmpeg && apt autoclean -y && rm -rf /var/lib/apt/lists/*

COPY --from=build-server /build/dist/swingmusic /swingmusic

RUN chmod +x /swingmusic

EXPOSE 1970/tcp

VOLUME /music
VOLUME /config

ENTRYPOINT ["/swingmusic", "--host", "0.0.0.0", "--config", "/config"]
