from .base import db
from datetime import datetime


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column('id', db.Integer, primary_key=True)
    label = db.Column('label', db.String(80),  index=True, nullable=False)
    topic_id = db.Column(
        'topic_id',
        db.Integer,
        db.ForeignKey('topics.id'),
        nullable=False
    )
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
    documents = db.relationship('Document', backref='tags', lazy=True)

    def __repr__(self):
        return '<Tag %r>' % self.label

    def __init__(self, label, topic_id):
        super()
        self.label = label
        self.topic_id = topic_id
