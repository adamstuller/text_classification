from flask import Blueprint, request, jsonify, current_app, make_response
import os
from app.machine_learning.predict import predict_tag
from app.machine_learning.train import get_all
from app.tasks import train_pipeline_task
from app.config import config, BANKS, PEPCO, predict_schema, train_schema
from jsonschema import validate, ValidationError, SchemaError 
import joblib


machine_learning_bp = Blueprint("machine_learning", __name__)
pipes = {
    BANKS: joblib.load(os.path.join(
        config['path_to_models'][BANKS], config['pipeline'][BANKS])),
    PEPCO: joblib.load(os.path.join(
        config['path_to_models'][PEPCO], config['pipeline'][PEPCO]))
}


@machine_learning_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    current_app.logger.error(e.message)
    return jsonify({
        'error': e.message
    }), 400


@machine_learning_bp.route('/api/v1/classification/predict', methods=['POST'])
def predict():

    data = request.get_json()
    validate(instance=data, schema=predict_schema)

    current_app.logger.info(data)
    prediction = predict_tag(pipes[data['topic']], **data)
    current_app.logger.info(prediction)
    return {
        'message': 'predicted successfully',
        'payload': prediction
    }


@machine_learning_bp.route('/api/v1/classification/training/pipeline/<topic_type>', methods=['POST'])
def process_pipeline_endpoint(topic_type):

    data = request.get_json()
    validate(instance=data, schema=train_schema)

    current_app.logger.info(data)
    pipeline_name = data['pipeline_name']

    train_pipeline_task.delay(
        pipeline_name=pipeline_name,
        topic_type=topic_type
    )
    return {
        'message': 'training new pipeline',
        'payload': data
    }


@machine_learning_bp.route('/api/v1/classification/training/pipeline/<topic_type>', methods=['GET'])
def process_pipeline_listing(topic_type):
    current_app.logger.info(topic_type)
    return {
        'message': 'pipelines got successfully',
        'payload': get_all('pipeline',  topic_type)
    }


@machine_learning_bp.route('/api/v1/classification/training/dataset/<topic_type>', methods=['GET'])
def process_dataset_endpoint(topic_type):

    if request.method == 'GET':
        return {
            'message': 'datasets got successfully',
            'payload': get_all('dataset', topic_type=topic_type)
        }
