
ppath=$(poetry run which python)

$ppath manage.py


#python manage.py

# gunicorn -b 0.0.0.0:9876 --workers=4 "wsgi:create_app()" --log-level=debug
