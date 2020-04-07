from .base import workflows_bp
from flask import request, current_app
from app.models import Topic, Document, Tag
from jsonschema import validate, ValidationError, SchemaError 
from app.config import create_topic_schema
from io import StringIO
import pandas as pd
from pandas.io.json import build_table_schema
def create_topic(dataset: pd.DataFrame, name: str, tags: list, mailto: str):
    pass


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
        # data = request.get_json()
        # validate(instance=data, schema=create_topic_schema)
        dataset = pd.read_csv(request.files.get('dataset'))

        current_app.logger.info(build_table_schema(dataset))
        current_app.logger.info(request.form.values)

        # return create_topic(data)
        return 'jupi'
    elif request.method == 'UPDATE':
        return update_topic()
