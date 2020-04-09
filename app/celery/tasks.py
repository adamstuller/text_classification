from app import celery
from app.machine_learning.train import train_pipe
from app.config import config
import pandas as pd
from app.models import Topic, Document, Tag, db
from celery.utils.log import get_task_logger
from app.machine_learning.preprocessing import NLP4SKSimplePreprocesser
from app.machine_learning.evaluation import evaluate
from functools import reduce
from app.helpers import dict_to_map

logger = get_task_logger(__name__)
# TODO: PREROBIT ASYNCHRONNE


@celery.task()
def evaluate_model_task(topic_id):

    try:
        matching_documents = Topic\
            .get_matching_documents(
                topic_id,
                [
                    Document.updated_sentence,
                    Document.sentiment_percentage,
                    Document.post_id,
                    Document.parent_tag,
                    Document.likes,
                    Tag.label.label('tag')
                ]
            )

        df = pd.DataFrame(matching_documents)
        result = evaluate(df)
        topic = Topic.query.get(topic_id)
        topic.f1_macro = result['f1_macro']
        topic.f1_weighted = result['f1_weighted']
        topic.recall = result['recall']
        topic.precision = result['precision']
        topic.accuracy = result['accuracy']
        db.session.commit()
        logger.info(result)
    except:
        logger.error('Error occured by evaluating model')
    return topic_id


@celery.task()
def train_pipeline_task(topic_id):
    matching_documents = Topic\
        .get_matching_documents(
            topic_id,
            [
                Document.updated_sentence,
                Document.sentiment_percentage,
                Document.post_id,
                Document.parent_tag,
                Document.likes,
                Tag.label.label('tag')
            ]
        )

    df = pd.DataFrame(matching_documents)
    df = df[df['updated_sentence'].notna()]

    topic = Topic.query\
        .get(topic_id)

    topic.pipeline = train_pipe(df.drop(columns=['tag']), df.tag)

    db.session.commit()
    return topic_id


@celery.task()
def nlp4sk_topic_task(topic_id):

    matching_documents = Tag.query\
        .join(Document)\
        .filter(Tag.topic_id == topic_id)\
        .filter(Document.updated_sentence == None)\
        .with_entities(Document.id, Document.sentence)\
        .all()

    nlp4sk = NLP4SKSimplePreprocesser('sentence')
    updated_matching_sentences = nlp4sk.transform(matching_documents)

    # Structure must be changed to {id: updated_sentence}
    updated_matching_sentences = dict_to_map(
        updated_matching_sentences,
        'id',
        'updated_sentence'
    )

    updated_ids = list(updated_matching_sentences.keys())

    for uid in updated_ids:
        doc = Document.query\
            .get(uid)
        doc.updated_sentence = updated_matching_sentences[uid]

    topic = Topic.query.get(topic_id)
    topic.updated = True

    db.session.commit()

    return topic_id


@celery.task()
def create_topic_task(df, name: str, desc: str):

    logger.info(df)

    df = pd.read_json(df)

    unique_tags = list(df.tag.unique())

    topic = Topic(
        name=name,
        description=desc,
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

    original = topic.tags
    new_tags = list(df.tag.unique())

    for tag in [x for x in new_tags if x in original]:
        matching_documents = df[df.tag == tag.label]

        tag.documents.extend(
            matching_documents.apply(
                lambda x: Document(
                    x.sentence,
                    None,
                    x.sentiment_percentage,
                    x.post_id,
                    x.parent_tag,
                    x.likes
                ),
                axis=1
            )
        )

    topic.updated = False
    db.session.commit()
    return topic.id
