
from app import celery
from app.factory import create_app
from app.celery.celery_utils import init_celery
app = create_app( db=True)
init_celery(celery, app)