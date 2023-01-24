#!/bin/zsh

gpath=$(poetry run which gunicorn)
# pytest=$(poetry run which pytest)

# $pytest # -q

echo "Starting swing"
"$gpath" -b 0.0.0.0:1970 --threads=2 "manage:create_api()"
