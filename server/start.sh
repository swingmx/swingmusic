# ppath=$(poetry run which python)

# $ppath manage.py

#python manage.py

gpath=$(poetry run which gunicorn)
while getopts ':s' opt; do
  case $opt in
    s)
      echo "Starting Alice server"
      cd "./app"
      "$gpath" -b 0.0.0.0:9877 -w 4 --threads=2 "imgserver:app" &
      cd ../
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

"$gpath" -b 0.0.0.0:9876 -w 1 --threads=4 "manage:create_app()"
