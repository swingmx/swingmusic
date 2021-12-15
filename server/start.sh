export PORT=8000
export music_dir="/home/cwilvx/Music/"

# export FLASK_APP=app
# export FLASK_DEBUG=1
# export FLASK_RUN_PORT=8008

# export music_dirs="['/home/cwilvx/Music/', '/home/cwilvx/FreezerMusic']"

# flask run

python manage.py

# gunicorn -b 0.0.0.0:9876 --workers=4 "wsgi:create_app()" --log-level=debug