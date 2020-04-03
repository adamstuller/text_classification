from app.models.tag import Tag
from app.models.topic import Topic
from app.models.document import Document

from .base import db

def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
