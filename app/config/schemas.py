from app.config import config
from app.config import BANKS, PEPCO, POSTED_BY_COLUMN_NAME, SENTENCE_COLUMN_NAME, SENTIMENT_PERCENTAGE_COLUMN_NAME, POST_ID_COLUMN_NAME, PARENT_CLASS_COLUMN_NAME, LIKES_COLUMN_NAME

predict_schema = {
    'required': [SENTENCE_COLUMN_NAME, LIKES_COLUMN_NAME, SENTIMENT_PERCENTAGE_COLUMN_NAME, POST_ID_COLUMN_NAME, POSTED_BY_COLUMN_NAME, 'topic'],
    'properties': {
        'topic':  {
            'type':  'string',
            'enum': config['available_topics'],
            'default': BANKS
        },
        SENTENCE_COLUMN_NAME: {'type': 'string'},
        LIKES_COLUMN_NAME: {'type': 'integer'},
        SENTIMENT_PERCENTAGE_COLUMN_NAME: {'type': 'number'},
        POST_ID_COLUMN_NAME: {'type': 'integer'},
        POSTED_BY_COLUMN_NAME: {
            'type': 'integer',
            'enum': [0, 1],
            'default': 0
        }
    },
    "allOf": [
        {
            "if": {
                "properties": {"topic": {"const": BANKS}}
            },
            "then": {
                "properties": {PARENT_CLASS_COLUMN_NAME: {
                    'type': 'string',
                    'enum': config['classes'][BANKS]
                }}
            }
        },
        {
            "if": {
                "properties": {"topic": {"const": PEPCO}}
            },
            "then": {
                "properties": {PARENT_CLASS_COLUMN_NAME: {
                    'type': 'string',
                    'enum': config['classes'][PEPCO]
                }}
            }
        }
    ]
}

train_schema = {
    'type': 'object',
    'properties': {
        'pipeline_name': {'type': 'string'},
    },
    "additionalProperties": False
}

create_topic_schema = {
    'properties': {
        'name': {
            'type': 'string'
        },
        'classes': {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        'mailto': {
            'type': 'string'
        }
    }
}
