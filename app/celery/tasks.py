from app import celery
from app.machine_learning.train import train_pipe
from app.config import config
import pandas as pd
from app.models import Topic, Document, Tag, db
from celery.utils.log import get_task_logger
from app.machine_learning.preprocessing import NLP4SKPreprocesser
from app.machine_learning.evaluation import evaluate
from functools import reduce
from app.helpers import dict_to_map
from app.mail import send_mail_train_finished_notification

logger = get_task_logger(__name__)
# TODO: PREROBIT ASYNCHRONNE


@celery.task()
def send_confirmation_email_task(params):

    topic_id = params['topic_id']
    mailto = params['mailto']

    if mailto is None:
        logger.info('mailto not set... no notification is being sent')
        return topic_id

    topic = Topic.query.get(topic_id)
    result = {
        'name': topic.name,
        'description': topic.description,
    }

    if topic.f1_macro:
        result = {
            **result,
            'evaluation': {
                'f1_macro': topic.f1_macro,
                'f1_weighted': topic.f1_weighted,
                'recall': topic.recall,
                'precision': topic.precision,
                'accuracy': topic.accuracy,
            }
        }

    try:
        res = send_mail_train_finished_notification(
            mailto,
            result
        )
        logger.info(res)
    except Exception as e:
        logger.error(e)

    return params

@celery.task()
def evaluate_model_task(params):

    topic_id = params['topic_id']

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
        df = df[df['updated_sentence'].notna()]
        
        result = evaluate(df)
        topic = Topic.query.get(topic_id)
        topic.f1_macro = result['f1_macro']
        topic.f1_weighted = result['f1_weighted']
        topic.recall = result['recall']
        topic.precision = result['precision']
        topic.accuracy = result['accuracy']
        db.session.commit()
        logger.info(result)
    except Exception as e:
        logger.error(f'Error occured by evaluating model: {e}')
    return params


@celery.task()
def train_pipeline_task(params):

    topic_id = params['topic_id']

    matching_documents = Topic.get_matching_documents(
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
    return params


@celery.task()
def nlp4sk_topic_task(params):

    topic_id = params['topic_id']

    matching_documents = Tag\
        .query\
        .join(Document)\
        .filter(Tag.topic_id == topic_id)\
        .filter(Document.updated_sentence == None)\
        .with_entities(
            Document.sentence,
            Document.id
        )\
        .all()

    matching_documents = list(map(
        lambda x: x._asdict(),
        matching_documents
    ))

    nlp4sk = NLP4SKPreprocesser('sentence')

    updated_matching_sentences = nlp4sk.transform(matching_documents)

    for ums in updated_matching_sentences:
        doc = Document.query\
            .get(ums['id'])

        doc.updated_sentence = ums['updated_sentence']

    topic = Topic.query.get(topic_id)
    topic.updated = True

    db.session.commit()

    return params


@celery.task()
def create_topic_task(df, params):

    name = params['topic_name']
    desc = params['topic_desc']

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

    return {
        'topic_id': topic.id,
        **params
    }


@celery.task()
def update_topic_task(df: pd.DataFrame, params):
    df = pd.read_json(df)

    topic_name = params['topic_name']

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
    return {
        'topic_id': topic.id,
        **params
    }
