from .base import db
from .tag import Tag
from .document import Document
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
    f1_macro = db.Column('f1_macro', db.Float)
    f1_weighted = db.Column('f1_weighted', db.Float)
    recall = db.Column('recall', db.Float)
    precision = db.Column('precision', db.Float)
    accuracy = db.Column('accuracy', db.Float)
    description = db.Column('description', db.Text)

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
        pipeline_result = cls.query\
            .filter(topic_name == Topic.name)\
            .with_entities(Topic.pipeline)\
            .first()

        return pipeline_result[0] if pipeline_result is not None else None

    @classmethod
    def get_matching_documents(cls, topic_id, entities):
        matching_documents = cls.query\
            .join(Tag)\
            .join(Document)\
            .filter(cls.id == topic_id)\
            .with_entities(*entities)\
            .all()

        return list(map(
            lambda x: x._asdict(),
            matching_documents
        ))

    @classmethod
    def get_all_topics(cls, entities):
        all_topics = cls.query\
            .with_entities(*entities)\
            .all()

        return list(map(
            lambda x: x._asdict(),
            all_topics
        ))

    @classmethod
    def find_by_name(cls,  topic_name):
        return Topic.query\
            .filter(cls.name  ==  topic_name)\
            .first()


    def __repr__(self):
        return '<Topic %r>' % self.name

    def __init__(self, name, description, updated=False,  tags=[]):
        super()
        self.name = name
        self.description = description
        self.updated = updated
        self.tags = tags
