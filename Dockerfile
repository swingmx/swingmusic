FROM node:latest AS CLIENT

RUN git clone --depth 1 https://github.com/swing-opensource/swingmusic-client.git client

WORKDIR /client

# RUN git checkout $(git describe --tags $(git rev-list --tags --max-count=1))

RUN yarn install

RUN yarn build

FROM python:latest

WORKDIR /app/swingmusic

COPY . .

COPY --from=CLIENT /client/dist/ client

EXPOSE 1970/tcp

VOLUME /music

VOLUME /config

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

RUN apt-get update && apt-get install -y ffmpeg libavcodec-extra

ENTRYPOINT ["poetry", "run", "python", "manage.py", "--host", "0.0.0.0", "--config", "/config"]