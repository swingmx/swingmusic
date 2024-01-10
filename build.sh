#!/bin/zsh

# builds the latest version of the client and server

git submodule update --init
cd swingmusic-client
yarn build --outDir ../client

cd ..
poetry run python manage.py --build
