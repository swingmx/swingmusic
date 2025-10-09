FROM python:3.11-slim
WORKDIR /app/swingmusic

# Copy the files in the current dir into the container
# copy wheelhouse
COPY wheels wheels

LABEL "author"="swing music"
EXPOSE 1970/tcp
VOLUME /music
VOLUME /config

RUN apt-get update && apt-get install -y python3-dev ffmpeg libavcodec-extra && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --find-links=wheels/ swingmusic
Run rm -rf /app/swingmusic/wheels

ENTRYPOINT ["python", "-m", "swingmusic", "--host", "0.0.0.0", "--config", "/config"]
