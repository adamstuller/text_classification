from .base import workflows_bp
from flask import request, current_app
from app.models import Topic, Document, Tag
from jsonschema import validate, ValidationError, SchemaError
import pandas as pd
from app.machine_learning.preprocessing import NLP4SKSimplePreprocesser
from app.machine_learning.predict import predict_tag
from app.config import predict_schema

nlp4sk = NLP4SKSimplePreprocesser('sentence')


@workflows_bp.route('/api/v1/topics/<topic_name>', methods=['GET'])
def handle_single_topic(topic_name):
    pass


@workflows_bp.route('/api/v1/topics/<topic_name>/predict', methods=['POST'])
def handle_predict(topic_name):

    data = request.json
    dataset = data['dataset']
    #TODO: VALIDACIA
    # TODO: MAX 100
    validate(instance=data, schema=predict_schema)

    prediction = predict_tag(
        Topic.get_pipeline_by_name(topic_name),
        nlp4sk.transform(dataset)
    )

    return {
        'message': 'predicted successfully',
        'payload': prediction
    }
