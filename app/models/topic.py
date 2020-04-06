from .base import db

class Topic(db.Model):
    # tablename = 'topics'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(20), index=True)
    pipeline_name = db.Column('pipeline_name',  db.String(20), index=True)
    created_at = db.Column('created_at', db.DateTime)
    updated_at = db.Column('updated_at', db.DateTime)