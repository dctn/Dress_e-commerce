web: python manage.py migrate \
     && python manage.py collectstatic --noinput \
     && gunicorn e_commerce_site.wsgi:application \
            --bind 0.0.0.0:$PORT \
            --log-file -