web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn exam_form_system.wsgi:application --bind 0.0.0.0:$PORT
