from app import celery
from app.machine_learning.train import  train_pipe
from app.config import config
import pandas as pd
from app.models import Topic, Document, Tag, db
from celery.utils.log import get_task_logger
from app.machine_learning.preprocessing import NLP4SKSimplePreprocesser
from functools import reduce

logger = get_task_logger(__name__)


@celery.task()
def train_pipeline_task(topic_id):
    matching_documents = Tag.query\
        .join(Document)\
        .filter(Tag.topic_id == topic_id)\
        .with_entities(
            Document.updated_sentence,
            Document.sentiment_percentage,
            Document.post_id,
            Document.parent_tag,
            Document.likes,
            Tag.label.label('tag')
        )\
        .all()

    matching_documents = list(map(
        lambda x: x._asdict(),
        matching_documents
    ))

    df = pd.DataFrame.from_dict(matching_documents)

    topic = Topic.query\
        .get(topic_id)

    topic.pipeline = train_pipe(df)

    db.session.commit()
    return topic_id


@celery.task()
def nlp4sk_topic_task(topic_id):

    matching_sentences = Tag.query\
        .join(Document)\
        .filter(Tag.topic_id == topic_id)\
        .filter(Document.updated_sentence == None)\
        .with_entities(Document.id, Document.sentence)\
        .all()

    matching_sentences = list(map(
        lambda x: x._asdict(),
        matching_sentences
    ))

    nlp4sk = NLP4SKSimplePreprocesser('sentence')
    updated_matching_sentences = nlp4sk.transform(matching_sentences)

    #Structure must be changed to {id: updated_sentence}
    updated_matching_sentences = reduce(
        lambda acc, x: {
            **acc,
            **{x['id']:x['updated_sentence'] }
        },
        updated_matching_sentences,
        {}
    )
    updated_ids = list(updated_matching_sentences.keys())

    for uid in updated_ids:
        logger.info(uid)
        doc = Document.query\
            .get(uid)
        doc.updated_sentence = updated_matching_sentences[uid]

    topic = Topic.query.get(topic_id)
    topic.updated = True

    db.session.commit()

    return topic_id


@celery.task()
def create_topic_task(df, name: str):

    logger.info(df)

    df = pd.read_json(df)

    unique_tags = list(df.tag.unique())

    topic = Topic(
        name=name,
        pipeline_name=f'{name}-pipeline',
        updated=False
    )

    topic.tags = list(map(
        lambda x: Tag(
            label=x,
            topic_id=topic.id

        ),
        unique_tags
    ))

    for tag in topic.tags:
        tag.documents = df[df.tag == tag.label]\
            .apply(lambda x: Document(
                x.sentence,
                None,
                x.sentiment_percentage,
                x.post_id,
                x.parent_tag,
                x.likes
            ), axis=1
        )

    db.session.add(topic)
    db.session.commit()

    return topic.id


@celery.task()
def update_topic_task(df: pd.DataFrame, topic_name: str):
    df = pd.read_json(df)

    topic = Topic.query\
        .filter(Topic.name == topic_name)\
        .first()

    unique_tags = topic.tags

    for tag in topic.tags:
        tag.documents.extend(df[df.tag == tag.label]\
            .apply(lambda x: Document(
                x.sentence,
                None,
                x.sentiment_percentage,
                x.post_id,
                x.parent_tag,
                x.likes
            ), axis=1
        ))

    topic.updated = False
    db.session.commit()
    return topic.id
    