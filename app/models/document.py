from .base import db


class Document(db.Model):
    # tablename = 'documents'
    id = db.Column('id', db.Integer, primary_key=True)
    sentence = db.Column('sentence', db.Text, index=True)
    updated_sentence = db.Column('updated_sentence', db.Text, index=True)
    sentiment_percentage = db.Column('sentiment_percentage', db.Float)
    post_id = db.Column('post_id', db.Integer)
    parent_class = db.Column('parent_class', db.Integer)
    likes = db.Column('likes', db.Integer)
    tag_id = db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
    created_at = db.Column('created_at', db.DateTime)
    updated_at = db.Column('updated_at', db.DateTime)

    def __repr__(self):
        return '<Document %r>' % self.name