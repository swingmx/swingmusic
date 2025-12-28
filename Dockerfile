ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

LABEL "author"="swing music"
LABEL "description"="Swing Music is a beautiful, self-hosted music player for your local audio files. Like a cooler Spotify ... but bring your own music."

# Default user and group IDs
ENV PUID=1000 \
    PGID=1000 \
    USER_NAME=swingmusic

EXPOSE 1970/tcp
VOLUME /music
VOLUME /config

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libev-dev \
        libc6-dev \
        ffmpeg \
        libavcodec-extra \
        gosu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN groupadd -g ${PGID} ${USER_NAME} \
    && useradd -u ${PUID} -g ${PGID} -m ${USER_NAME}

COPY pyproject.toml requirements.txt version.txt README.md* ./
COPY src/ ./src/

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install .

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh", "python", "-m", "swingmusic", "--host", "0.0.0.0", "--config", "/config"]
