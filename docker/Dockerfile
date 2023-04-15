FROM node:16.19.0-alpine as client-build

RUN apk add git

WORKDIR /app

RUN git clone https://github.com/swing-opensource/swingmusic-client.git

WORKDIR /app/swingmusic-client

RUN yarn install

RUN yarn build

FROM python:3.10 as app-build

WORKDIR /application

RUN mkdir client

COPY --from=client-build /app/swingmusic-client/dist /application/client

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN mkdir $HOME/.config

COPY .. /application

RUN poetry install

EXPOSE 1970/tcp

VOLUME ["/root/.config/swingmusic", "/root/music"]

CMD ["poetry", "run", "python", "manage.py", "--host", "0.0.0.0"]
