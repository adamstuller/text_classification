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
from app.celery.tasks import create_topic_task, update_topic_task, train_save_pipeline_task, print_pipeline
from celery import chain




def update_topic():
    pass


@workflows_bp.route('/api/v1/models', methods=['GET', 'POST', 'UPDATE'])
def handle_models():

    if request.method == 'GET':
        return {
            'message': 'all topic retreived',
            'topics': Document.query.all()
        }
    elif request.method == 'POST':
        # TODO: BUDE TREBA ZVALIDOVAT FORM
        dataset = process_csv(request.files.get('dataset'), column_names=None)
        topic_name = request.form.get('name')
        chain(
            create_topic_task.signature(),
            update_topic_task.signature(),
            train_save_pipeline_task.signature()
        ).delay(dataset.to_json(), topic_name)
        

        # return create_topic(data)
        return 'jupi'
    elif request.method == 'UPDATE':
        return update_topic()
