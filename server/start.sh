# ppath=$(poetry run which python)

# $ppath manage.py

#python manage.py

gpath=$(poetry run which gunicorn)
cd app
"$gpath" -b 0.0.0.0:9877 -w 4 --threads=2 "imgserver:app" &
echo "Booted image server"
cd ../
"$gpath" -b 0.0.0.0:9876 -w 1 --threads=4 "manage:create_app()" #--log-level=debug

