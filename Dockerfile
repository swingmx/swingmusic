FROM node:latest AS CLIENT

ARG client_tag

RUN git clone --branch $client_tag --depth 1 https://github.com/swing-opensource/swingmusic-client.git client

WORKDIR /client

# RUN git checkout $(git describe --tags $(git rev-list --tags --max-count=1))
# checkout the latest tag
# RUN git checkout $client_tag

RUN yarn install

RUN yarn build

FROM python:3.10

WORKDIR /app/swingmusic

COPY . .

COPY --from=CLIENT /client/dist/ client

EXPOSE 1970/tcp

VOLUME /music

VOLUME /config

RUN mkdir -p /root/.cache/pypoetry/virtualenvs

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

RUN apt-get update && apt-get install -y ffmpeg libavcodec-extra

ENTRYPOINT ["poetry", "run", "python", "manage.py", "--host", "0.0.0.0", "--config", "/config"]
