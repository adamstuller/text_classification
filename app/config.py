from os import path, getenv


class BaseConfig(object):
    'Base config class'
    DEBUG = True
    TESTING = False


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
    "path_to_models": path.join(path.dirname(path.realpath(__file__)), 'machine_learning', 'data', 'models'),
    "path_to_datasets": path.join(path.dirname(path.realpath(__file__)), 'machine_learning', 'data', 'datasets'),
    'path_to_banks_dataset': path.join(path.dirname(path.realpath(__file__)), 'machine_learning', 'data', 'datasets', 'banks.csv'),
    "classes": ['Neutral', 'Súťaž', 'Interakcia', 'Ostatné', 'Ponuka produktov',
                'Cena produktov / benefity', 'Problémy s produktom', 'Odpovede',
                'Produkt', 'Otázky', 'Pobočka'],
    'pipeline': 'pipeline-2020-03-28.joblib',
    'redis_url': getenv('REDIS_URL', 'localhost')
}
