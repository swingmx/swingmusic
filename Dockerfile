FROM python:3.11-slim
WORKDIR /app

LABEL "author"="swing music"
EXPOSE 1970/tcp
VOLUME /music
VOLUME /config

RUN apt-get update 

RUN apt-get install -y gcc libev-dev 
RUN apt-get install -y ffmpeg libavcodec-extra 
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy repo root files needed for installation
COPY pyproject.toml requirements.txt version.txt ./ 
COPY src/ ./src/

# Install the package and its dependencies
RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "swingmusic", "--host", "0.0.0.0", "--config", "/config"]
