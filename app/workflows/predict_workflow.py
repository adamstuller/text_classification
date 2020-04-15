from .base import workflows_bp
from flask import request, current_app, jsonify
from app.models import Topic, Document, Tag
from jsonschema import validate, ValidationError, SchemaError
import pandas as pd
from app.machine_learning.preprocessing import NLP4SKPreprocesser
from app.machine_learning.predict import predict_tag
from app.config import predict_schema
from app.helpers import DefaultValidatingDraft7Validator
from copy import deepcopy
from werkzeug.exceptions import NotFound


nlp4sk = NLP4SKPreprocesser('sentence')


@workflows_bp.route('/api/v1/topics/<topic_name>', methods=['GET'])
def handle_single_topic(topic_name):
    topic = Topic.query\
        .filter(Topic.name == topic_name)\
        .with_entities(
            Topic.name,
            Topic.description,
            Topic.accuracy,
            Topic.f1_macro,
            Topic.f1_weighted,
            Topic.recall,
            Topic.precision,
            Topic.updated
        )\
        .first()
    
    if topic is not None:
        return  topic._asdict()
    else:
        raise NotFound(f'Topic {topic_name} does not exist')


@workflows_bp.route('/api/v1/topics/<topic_name>/predict', methods=['POST'])
def handle_predict(topic_name):

    data = request.json

    DefaultValidatingDraft7Validator(predict_schema)\
        .validate(data)

    current_app.logger.info(data)

    dataset = data['dataset']

    pipeline  = Topic.get_pipeline_by_name(topic_name)
    if pipeline is None:
        raise NotFound(f'Topic {topic_name} does not exist')

    prediction = predict_tag(
        pipeline,
        nlp4sk.transform(dataset)
    )

    return {
        'message': 'predicted successfully',
        'payload': prediction
    }
