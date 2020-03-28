from flask import Blueprint, request, jsonify, current_app
import os
from app.machine_learning.predict import predict_tag
from app.config import config
import joblib



# from app.tasks import make_file
machine_learning_bp = Blueprint("machine_learning", __name__)
pipe = joblib.load(os.path.join(config['path_to_models'], config['pipeline']))


@machine_learning_bp.route('/api/v1/classification/predict', methods=['POST'])
def predict():
    data = request.get_json()
    current_app.logger.info(data)
    prediction = predict_tag(pipe, **data)
    current_app.logger.info(prediction)
    return prediction
