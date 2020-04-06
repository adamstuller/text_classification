
from app import celery
from app.factory import create_app
from app.celery.celery_utils import init_celery
app = create_app()
init_celery(celery, app)