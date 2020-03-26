from flask import Flask, request, jsonify
from flask_json_schema import JsonSchema, JsonValidationError
import os
from app.config import config
from logging.config import dictConfig
from dotenv import load_dotenv
from app.schemas import predict_schema, train_schema
from app.predict import predict_tag
from app.train import train_pipeline
from joblib import load
load_dotenv()

dictConfig(config['logger'])

app = Flask(__name__)
schema = JsonSchema(app)


@app.errorhandler(JsonValidationError)
def validation_error(e):
    app.logger.error({"message": e.message})
    return jsonify({'error': e.message, 'errors': [validation_error.message for validation_error in e.errors]})


@app.route('/api/v1/classification/predict', methods=['POST'])
@schema.validate(predict_schema)
def predict():
    data = request.get_json()
    app.logger.info(data)
    return predict_tag(pipe, **data)


@app.route('/api/v1/classification/train', methods=['POST'])
@schema.validate(train_schema)
def train():
    train_pipeline()
    return (200)


app.config.from_object(config['flask'][os.environ['FLASK_ENV']])
