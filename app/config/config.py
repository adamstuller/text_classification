from os import path, getenv

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
    'redis_url': getenv('REDIS_URL', 'localhost'),
    'database': {
        'create_on_start': getenv('DATABASE__CREATE_ON_START', 'False') == 'True'
    },
    'sendgrid': {
        'api_key': getenv('SENDGRID_API_KEY'),
        'mailfrom': 'textclassification@periskop.life'
    },
    'min_database_size': 100,
    # 'min_tag_size': 4,
    'limit_tag_size': 20
}
