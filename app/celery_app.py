import os

try:
    from celery import Celery
except ImportError:  # Celery is optional for local development.
    Celery = None


def make_celery(app_name=__name__):
    if Celery is None:
        return None

    broker = os.getenv("CELERY_BROKER_URL")
    backend = os.getenv("CELERY_RESULT_BACKEND")
    if not broker:
        return None

    return Celery(app_name, broker=broker, backend=backend)
