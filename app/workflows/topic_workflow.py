from .base import workflows_bp
from flask import request, current_app
from app.models import Topic, Document, Tag
from jsonschema import validate, ValidationError, SchemaError
from app.config import create_topic_schema
from io import StringIO
import pandas as pd
from pandas.io.json import build_table_schema
from app.helpers import process_csv
from app.config import COLUMN_NAMES
from app.celery.tasks import create_topic_task, nlp4sk_topic_task, train_pipeline_task, update_topic_task
from celery import chain


#TODO: CHYBA NAM MAILTO 
#TODO: CHYBA NAM VALIDACIA MODELU

@workflows_bp.route('/api/v1/topics', methods=['GET', 'POST', 'PUT'])
def handle_topics():

    if request.method == 'GET':

        all_topics = Topic.query\
            .with_entities(Topic.name)\
            .all()
        return {
            'message': 'all topics retreived',
            'topics': all_topics
        }
    elif request.method == 'POST':
        # TODO: BUDE TREBA ZVALIDOVAT FORM
        dataset, topic_name = None, None

        if request.is_json:
            data = request.get_json()
            dataset = pd.DataFrame(data['dataset'])
            topic_name = data['name']
        else:
            dataset = process_csv(
                request.files.get('dataset'),
                column_names=None
            ) 
            topic_name = request.form.get('name')

        chain(
            create_topic_task.signature(),
            nlp4sk_topic_task.signature(),
            train_pipeline_task.signature()
        ).delay(dataset.to_json(), topic_name)

        return {
            'message': 'topic accepted, request is being handled'
        }, 202
    elif request.method == 'PUT':
        # TODO: BUDE TREBA ZVALIDOVAT FORM
        dataset, topic_name = None, None

        if request.is_json:
            data = request.get_json()
            dataset = pd.DataFrame(data['dataset'])
            topic_name = data['name']
        else:
            dataset = process_csv(
                request.files.get('dataset'),
                column_names=None
            )  
            topic_name = request.form.get('name')

        chain(
            update_topic_task.signature(),
            nlp4sk_topic_task.signature(),
            train_pipeline_task.signature()
        ).delay(dataset.to_json(), topic_name)

        return {
            'message': 'update accepted, request is being handled'
        }, 202
