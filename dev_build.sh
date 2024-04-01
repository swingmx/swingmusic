#!/bin/bash
# REVIEW Above: bash is way more compatible than other shells

# builds the latest version of the client and server

# NOTE Changes directory to the webclient directory and builds it
cd ../swingmusic-client || exit # REVIEW Failsafe exit
yarn build --outDir ../swingmusic/client
cd ../swingmusic || exit # REVIEW Failsafe exit

# REVIEW Optional cleaning up
# rm -rf build dist

# REVIEW Install poetry & requirements
# Build the app
poetry run python manage.py --build