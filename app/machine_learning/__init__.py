from flask import Blueprint
from os import path
from joblib import load
from app.config import config

bp = Blueprint('machine_learning', __name__)
# pipe = load(path.join(
#     config['path_to_models'], 'pipeline-2020-03-05.joblib'))
