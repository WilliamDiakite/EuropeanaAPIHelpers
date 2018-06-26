web: gunicorn app:app
worker: celery -A app:tasks.celery worker --loglevel=info
