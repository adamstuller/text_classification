from flask import Blueprint, request, jsonify, current_app
import os
from app.machine_learning.predict import predict_tag
from app.machine_learning.train import get_all
from app.tasks import train_pipeline_task
from app.config import config
import joblib


machine_learning_bp = Blueprint("machine_learning", __name__)
pipe = joblib.load(os.path.join(config['path_to_models'], config['pipeline']))


@machine_learning_bp.route('/api/v1/classification/predict', methods=['POST'])
def predict():
    data = request.get_json()
    current_app.logger.info(data)
    prediction = predict_tag(pipe, **data)
    current_app.logger.info(prediction)
    return prediction


@machine_learning_bp.route('/api/v1/classification/training/pipeline', methods=['POST', 'GET'])
def process_pipeline_endpoint():

    if request.method == 'GET':
        return {
            'message': 'pipelines got successfully',
            'payload': get_all('pipeline')
        }
    else:
        return {'message': 'ahoj'}


@machine_learning_bp.route('/api/v1/classification/training/dataset', methods=['GET'])
def process_dataset_endpoint():

    if request.method == 'GET':
        return {
            'message': 'datasets got successfully',
            'payload': get_all('dataset')
        }
