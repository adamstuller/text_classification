from flask import Flask
import os
from app.celery.celery_utils import init_celery
from logging.config import dictConfig
from app.config import config
from dotenv import load_dotenv
from . import models

load_dotenv()


PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]
dictConfig(config['logger'])


def create_app(app_name=PKG_NAME, **kwargs):

    app = Flask(app_name)
    app.config.from_object(config['flask'][os.environ['FLASK_ENV']])

    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)
    
    from app.machine_learning import machine_learning_bp
    app.register_blueprint(machine_learning_bp)

    if kwargs.get('db') and kwargs.get('db') == True:
        models.init_app(app)
    

    @app.route('/')
    def check():
        return 'Helloworld'
    return app
