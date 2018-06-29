import os

CELERY_TASK_SERIALIZER = 'json'
BROKER_URL = os.getenv('REDIS_URL', 'redis://')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://')
