import os
from celery import Celery


def make_celery(app_name=__name__):
    broker = os.getenv('CELERY_BROKER_URL')
    backend = os.getenv('CELERY_RESULT_BACKEND')
    if not broker:
        return None

    celery = Celery(app_name, broker=broker, backend=backend)
    return celery
