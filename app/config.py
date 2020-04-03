from os import path, getenv
from app.constants import PEPCO, BANKS


DATABASE__USER = getenv('DATABASE__USER', 'postgres')
DATABASE__PWD = getenv('DATABASE__PWD', 'dbs')
DATABASE__HOST = getenv('DATABASE__HOST', 'localhost:5432')
DATABASE__DBS = getenv('DATABASE_DBS', 'devdb')


class BaseConfig(object):
    'Base config class'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = getenv(
        'SQLALCHEMY_DATABASE_URI',
        f'postgresql+psycopg2://{DATABASE__USER}:{DATABASE__PWD}@{DATABASE__HOST}/{DATABASE__DBS}'
    )


class ProductionConfig(BaseConfig):
    'Production specific config'
    DEBUG = False


class StagingConfig(BaseConfig):
    'Staging specific config'
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    'Development environment specific config'
    DEBUG = True
    TESTING = True
    DEVELOPMENT = True


config = {
    'flask': {
        'development': 'app.config.DevelopmentConfig',
        'staging': 'app.config.StagingConfig',
        "production": "app.config.ProductionConfig",
        "default": "app.config.DevelopmentConfig"
    },
    'logger': {
        'version': 1,
        'formatters': {
            'default': {
                'format': '{"timestamp":"%(asctime)s","level":"%(levelname)s","module":"%(module)s","message":"%(message)s"}',
            }
        },
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    },
    "path_to_models": {
        BANKS: path.join(path.dirname(path.realpath(__file__)), 'machine_learning', 'data',  'models', BANKS),
        PEPCO: path.join(path.dirname(path.realpath(__file__)), 'machine_learning', 'data', 'models', PEPCO),
    },
    "path_to_datasets": {
        BANKS: path.join(path.dirname(path.realpath(__file__)), 'machine_learning', 'data', 'datasets', BANKS),
        PEPCO: path.join(path.dirname(path.realpath(__file__)),
                         'machine_learning', 'data', 'datasets', PEPCO)
    },
    "classes": {
        BANKS: ['Neutral', 'Súťaž', 'Interakcia', 'Ostatné', 'Ponuka produktov',
                'Cena produktov / benefity', 'Problémy s produktom', 'Odpovede',
                'Produkt', 'Otázky', 'Pobočka'],
        PEPCO: ['Quality', 'Unavailability of products', 'Offer of products',
                'Absent of e-shop', 'Lack of Pepco', 'Product', 'Interaction',
                'Price', 'Neutral', 'Other']
    },
    'pipeline': {
        PEPCO: 'pipeline-default.joblib',
        BANKS: 'pipeline-default.joblib'
    },
    'default_dataset': {
        PEPCO: 'updated_pepco',
        BANKS: 'updated_banks'
    },
    'redis_url': getenv('REDIS_URL', 'localhost'),
    'available_topics': [BANKS,  PEPCO],
    'database': {
        'create_on_start': getenv('DATABASE__CREATE_ON_START', 'False') ==  'True'
    }
}
