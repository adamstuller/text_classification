from app.models.tag import Tag
from app.models.topic import Topic
from app.models.document import Document
import numpy
from psycopg2.extensions import register_adapter, AsIs
from os import environ

def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

from .base import db

def init_app(app):
    db.init_app(app)
    register_adapter(numpy.float64, addapt_numpy_float64)
    register_adapter(numpy.int64, addapt_numpy_int64)
    if environ.get('DATABASE__CREATE') == 'True':
        with app.app_context():
            db.create_all()
