#!/bin/zsh

gpath=$(poetry run which gunicorn)
# pytest=$(poetry run which pytest)

# $pytest # -q

while getopts ':s' opt; do
  case $opt in
    s)
      echo "Starting image server"
      cd "./app"
      "$gpath" -b 0.0.0.0:1971 -w 1 --threads=1 "imgserver:app" &
      cd ../
      echo "Done ✅"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

echo "Starting swing"
"$gpath" -b 0.0.0.0:1970 --threads=2 "manage:create_api()"

# poetry run pyinstaller -F  -n swing -y --add-data "assets:assets" --add-data="app/client:app/client"  --clean manage.py
