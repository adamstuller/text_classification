from .base import db
from datetime import datetime


class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column('id', db.Integer, primary_key=True)
    sentence = db.Column('sentence', db.Text, index=True, nullable=False)
    updated_sentence = db.Column('updated_sentence', db.Text, index=True)
    sentiment_percentage = db.Column('sentiment_percentage', db.Float)
    post_id = db.Column('post_id', db.Integer)
    parent_tag = db.Column('parent_class', db.String(20))
    likes = db.Column('likes', db.Integer)
    tag_id = db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
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

    def __repr__(self):
        return '<Document %r>' % self.name

    def __init__(self, sentence, updated_sentence, sentiment_percentage, post_id, parent_class, likes):
        super()
        self.sentence = sentence
        self.updated_sentence = updated_sentence
        self.sentiment_percentage = sentiment_percentage
        self.post_id = post_id
        self.parent_class = parent_class
        self.likes = likes
