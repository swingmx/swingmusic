#!/bin/zsh

# builds the latest version of the client and server

cd ../swingmusic-client
yarn build --outDir ../swingmusic/client

cd ../swingmusic
poetry run python manage.py --build