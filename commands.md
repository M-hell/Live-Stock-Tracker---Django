uvicorn livestocktracker.asgi:application --host 127.0.0.1 --port 8000 --reload

celery -A livestocktracker.celery worker -l info -P solo

celery -A livestocktracker.celery beat -l info