
# ppath=$(poetry run which python)

# $ppath manage.py


#python manage.py
gpath=$(poetry run which gunicorn)


$gpath -b 0.0.0.0:9876 -w 1 --threads=4 "manage:create_app()" #--log-level=debug 
