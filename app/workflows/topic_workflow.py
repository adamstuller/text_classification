from .base import workflows_bp
from flask import request, current_app
from app.models import Topic, Document, Tag
from jsonschema import validate, ValidationError, SchemaError
from app.config import create_topic_schema
from io import StringIO
import pandas as pd
from pandas.io.json import build_table_schema
from app.helpers import process_csv
from app.config import config, COLUMN_NAMES
from app.celery.tasks import \
    create_topic_task, \
    nlp4sk_topic_task, \
    train_pipeline_task, \
    update_topic_task, \
    evaluate_model_task, \
    send_confirmation_email_task
from werkzeug.exceptions import BadRequest

from celery import chain


def handle_form(form, required):
    for item in required:
        if item not in form:
            raise BadRequest(f"'{item}' is a required property")


def handle_dataset(files):
    if 'dataset' not in files:
        raise BadRequest(f'\'dataset\' is a required property')
    df = process_csv(
        request.files.get('dataset'),
        column_names=None
    )

    return df

def columns_expected(df):
    return set(list(df.columns.unique())) == set(COLUMN_NAMES)

def minimal_size(df):
    return len(df) >= config['min_database_size']

def minimal_tag_size(df):
    return df.groupby('tag').count().sentence.ge(config['min_tag_size']).all()


def check_dataset_constraints(df: pd.DataFrame, method: str):
    if method == 'POST' and not minimal_size(df):
        raise BadRequest(
            f'Dataset is smaller than {config["min_database_size"]} entries, which is minimal size')

    if method == 'POST' and not minimal_tag_size(df):
        raise BadRequest(
            f'Not all of tags were in dataset at least {config["min_tag_size"]} times which is minimal required')

    if not columns_expected(df):
        raise BadRequest(
            f'Columns are not expected')


def check_topic_not_allocated(topic_name):
    topics = Topic.query\
        .filter(Topic.name == topic_name)\
        .all()
    if len(topics) > 0:
        raise BadRequest(
            f'Topic name {topic_name} is allready used, choose another'
        )


def check_topic_allocated(topic_name):
    topics = Topic.query\
        .filter(Topic.name == topic_name)\
        .all()
    if len(topics) == 0:
        raise BadRequest(
            f'Topic with name {topic_name} does not exists'
        )


@workflows_bp.route('/api/v1/topics', methods=['GET', 'POST', 'PUT'])
def handle_topics():

    if request.method == 'GET':

        all_topics = Topic.get_all_topics(
            [
                Topic.name,
                Topic.description,
                Topic.accuracy,
                Topic.f1_macro,
                Topic.f1_weighted,
                Topic.recall,
                Topic.precision,
                Topic.updated
            ]
        )
        return {
            'message': 'all topics retreived',
            'topics': all_topics
        }
    elif request.method == 'POST':
        # TODO: BUDE TREBA ZVALIDOVAT FORM
        dataset, topic_name, topic_desc, mailto = None, None, None, None

        if request.is_json:
            data = request.get_json()
            validate(instance=data, schema=create_topic_schema)

            dataset = pd.DataFrame(data['dataset'])
            topic_name = data['name']
            topic_desc = data['description']
            if 'mailto' in data:
                mailto = data['mailto']
        else:
            handle_form(request.form, ['name', 'description'])

            dataset = handle_dataset(request.files)
            topic_name = request.form.get('name')
            topic_desc = request.form.get('description')
            if 'mailto' in request.form:
                mailto = request.form.get('mailto')

        check_dataset_constraints(dataset, method='POST')
        check_topic_not_allocated(topic_name)
        chain(
            create_topic_task.signature(),
            nlp4sk_topic_task.signature(),
            train_pipeline_task.signature(),
            evaluate_model_task.signature(),
            send_confirmation_email_task.signature()
        ).delay(
            dataset.to_json(),
            {
                'topic_name': topic_name,
                'topic_desc': topic_desc,
                'mailto': mailto
            }
        )

        return {
            'message': 'topic accepted, request is being handled'
        }, 202
    elif request.method == 'PUT':
        # TODO: BUDE TREBA ZVALIDOVAT FORM
        dataset, topic_name,  mailto = None, None, None

        if request.is_json:
            data = request.get_json()
            validate(instance=data, schema=create_topic_schema)
            dataset = pd.DataFrame(data['dataset'])
            topic_name = data['name']
            if 'mailto' in data:
                mailto = data['mailto']
        else:
            handle_form(request.form, ['name'])
            dataset = handle_dataset(request.files)

            topic_name = request.form.get('name')
            if 'mailto' in request.form:
                mailto = request.form.get('mailto')

        check_dataset_constraints(dataset, method='PUT')
        check_topic_allocated(topic_name)
        chain(
            update_topic_task.signature(),
            nlp4sk_topic_task.signature(),
            train_pipeline_task.signature(),
            evaluate_model_task.signature(),
            send_confirmation_email_task.signature()
        ).delay(dataset.to_json(), {
            'topic_name': topic_name,
            'mailto': mailto
        })

        return {
            'message': 'update accepted, request is being handled'
        }, 202
