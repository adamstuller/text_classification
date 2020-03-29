from flask import Blueprint, request, jsonify, current_app, make_response
import os
from app.machine_learning.predict import predict_tag
from app.machine_learning.train import get_all
from app.tasks import train_pipeline_task
from app.config import config
from jsonschema import validate, ValidationError, SchemaError
from app.schemas import predict_schema, train_schema
import joblib


machine_learning_bp = Blueprint("machine_learning", __name__)
pipe = joblib.load(os.path.join(config['path_to_models'], config['pipeline']))


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
    prediction = predict_tag(pipe, **data)
    current_app.logger.info(prediction)
    return {
        'message': 'predicted successfully',
        'payload': prediction
    }


@machine_learning_bp.route('/api/v1/classification/training/pipeline', methods=['POST', 'GET'])
def process_pipeline_endpoint():

    if request.method == 'GET':
        return {
            'message': 'pipelines got successfully',
            'payload': get_all('pipeline')
        }
    elif request.method == 'POST':
        data = request.get_json()
        validate(instance=data, schema=train_schema)

        current_app.logger.info(data)
        dataset_name = data['dataset_name']
        pipeline_name = data['pipeline_name']
        
        train_pipeline_task.delay(
            dataset_name=dataset_name,
            pipeline_name=pipeline_name
        )
        return {
            'message': f'training new pipeline',
            'payload': data
        }


@machine_learning_bp.route('/api/v1/classification/training/dataset', methods=['GET'])
def process_dataset_endpoint():

    if request.method == 'GET':
        return {
            'message': 'datasets got successfully',
            'payload': get_all('dataset')
        }
