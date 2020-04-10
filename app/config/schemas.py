from app.config import config

predict_schema = {
    'type': 'object',
    'required': ['dataset'],
    'properties': {
        'dataset':
            {
                'type': 'array',
                'items': {
                    'required': ['sentence'],
                    'type': 'object',
                    'properties': {
                        'sentence': {'type': 'string'},
                        'likes': {'type': 'integer'},
                        'sentiment_percentage': {'type': 'number'},
                        'post_id': {'type': 'integer'},
                        'posted_by': {
                            'type': 'integer',
                            'enum': [0, 1],
                            'default': 0
                        },
                        'parent_tag': {'type': 'string'}
                    }
                }
            }

    }
}

create_topic_schema = {
    'required': ['name', 'dataset'],
    'properties': {
        'name': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'mailto': {
            'type': 'string',
            'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$'

        },
        'dataset': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'sentence': {'type': 'string'},
                    'likes': {'type': 'integer'},
                    'sentiment_percentage': {'type': 'number'},
                    'post_id': {'type': 'integer'},
                    'posted_by': {
                        'type': 'integer',
                        'enum': [0, 1],
                        'default': 0
                    },
                    'parent_tag': {'type': 'string'},
                    'tag': {'type': 'string'}
                }
            }
        }
    }
}

update_topic_schema = {
    'required': ['name'],
    'properties': {
        'name': {'type': 'string'},
        'mailto': {
            'type': 'string',
            'pattern': "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
        },
        'dataset': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'sentence': {'type': 'string'},
                    'likes': {'type': 'integer'},
                    'sentiment_percentage': {'type': 'number'},
                    'post_id': {'type': 'integer'},
                    'posted_by': {
                        'type': 'integer',
                        'enum': [0, 1],
                        'default': 0
                    },
                    'parent_tag': {'type': 'string'},
                    'tag': {'type': 'string'}
                }
            }
        }
    }
}
