FROM python:3.11-slim
WORKDIR /app/swingmusic

# Copy source code and client
COPY . .
COPY client /config/client


LABEL "author"="swing music"
EXPOSE 1970/tcp
VOLUME /music
VOLUME /config

RUN apt-get update && apt-get install -y gcc git libev-dev python3-dev ffmpeg libavcodec-extra && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "swingmusic", "--host", "0.0.0.0", "--config", "/config", "--client", "/config/client"]
