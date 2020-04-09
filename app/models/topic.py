from .base import db
from datetime import datetime


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(
        'name',
        db.String(20),
        index=True,
        nullable=False,
        unique=True
    )
    updated = db.Column(
        'updated',
        db.Boolean,
        nullable=False,
        default=False
    )
    pipeline = db.Column('pipeline', db.PickleType)
    created_at = db.Column(
        'created_at',
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at = db.Column(
        'updated_at',
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        onupdate=datetime.utcnow
    )
    tags = db.relationship('Tag', backref='topics', lazy=True)

    @classmethod
    def get_pipeline_by_name(cls, topic_name):
        pipeline, *_ = cls.query\
            .filter(topic_name == Topic.name)\
            .with_entities(Topic.pipeline)\
            .first()

        return pipeline

    def __repr__(self):
        return '<Topic %r>' % self.name

    def __init__(self, name, pipeline_name, updated=False,  tags=[]):
        super()
        self.name = name
        self.pipeline_name = pipeline_name
        self.updated = updated
        self.tags = tags
