from app.models.tag import Tag
from app.models.topic import Topic
from app.models.document import Document
from os import environ

from .base import db

def init_app(app):
    db.init_app(app)
    if environ.get('DATABASE__CREATE') == 'True':
        with app.app_context():
            db.create_all()
