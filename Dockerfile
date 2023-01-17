FROM ubuntu:jammy

RUN apt-get -y update && \
    apt-get -y install wget

WORKDIR /usr/src/app

RUN wget https://github.com/geoffrey45/swingmusic/releases/download/linux-beta/swingmusic
RUN chmod a+x ./swingmusic

SHELL ["/bin/bash", "-c"]

VOLUME /root/.swing
VOLUME /root/music

EXPOSE 1970/tcp

CMD ["./swingmusic", "--host", "0.0.0.0"]
