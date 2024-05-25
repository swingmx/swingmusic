FROM node:latest AS CLIENT

RUN git clone --depth 1 https://github.com/swing-opensource/swingmusic-client.git client

WORKDIR /client

# RUN git checkout $(git describe --tags $(git rev-list --tags --max-count=1))
# checkout the latest tag
# RUN git checkout $client_tag

RUN yarn install
RUN yarn build

FROM python:3.11-slim
WORKDIR /app/swingmusic

# Copy the files in the current dir into the container
COPY . .

COPY --from=CLIENT /client/dist/ client

EXPOSE 1970/tcp

VOLUME /music

VOLUME /config


RUN apt-get update && apt-get install -y gcc python3-dev -y ffmpeg libavcodec-extra gcc-aarch64-linux-gnu && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

ARG app_version
ENV SWINGMUSIC_APP_VERSION=$app_version

ENTRYPOINT ["python", "manage.py", "--host", "0.0.0.0", "--config", "/config"]
