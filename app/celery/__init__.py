from celery import Celery
from app.config import config

def make_celery(app_name=__name__):
    backend = f"redis://{config['redis_url']}:6379/0"
    broker = backend.replace("0", "1")
    return Celery(app_name, backend=backend, broker=broker)