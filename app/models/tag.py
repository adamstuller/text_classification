from .base import db

class Tag(db.Model):
    # tablename = 'tags'
    id = db.Column('id', db.Integer, primary_key=True)
    label = db.Column('label', db.String(80),  index=True)
    topic_id = db.Column('topic_id',
                         db.Integer, db.ForeignKey('topic.id'))
    created_at = db.Column('created_at', db.DateTime)
    updated_at = db.Column('updated_at', db.DateTime)