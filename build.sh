#!/bin/bash
# REVIEW Above: bash is way more compatible than other shells

# builds the latest version of the client and server

# REVIEW These are not useful if you dont have the source code
#cd ../swingmusic-client
#yarn build --outDir ../swingmusic/client
#../swingmusic

# REVIEW Cleaning up
rm -rf build dist

# REVIEW Install poetry & requirements
poetry || pip install poetry
poetry install --no-root

# Build the app
poetry run python manage.py --build