from .base import db
from datetime import date


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(20), index=True, nullable=False)
    updated = db.Column('updated', db.Boolean, nullable=False)
    pipeline_name = db.Column(
        'pipeline_name',
        db.String(30),
        nullable=False
    )
    pipeline = db.Column('pipeline', db.PickleType)
    created_at = db.Column('created_at', db.DateTime)
    updated_at = db.Column('updated_at', db.DateTime)
    tags = db.relationship('Tag', backref='topics', lazy=True)

    def __repr__(self):
        return '<Topic %r>' % self.name

    def __init__(self, name, pipeline_name, updated=False,  tags=[]):
        super()
        self.name = name
        self.pipeline_name = pipeline_name
        self.updated = updated
        self.tags = tags
        self.created_at = date.today()
        self.updated_at = date.today()
