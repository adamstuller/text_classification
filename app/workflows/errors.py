from .base import workflows_bp
from flask import current_app
from jsonschema import validate, ValidationError, SchemaError 


@workflows_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    current_app.logger.error(e.message)
    return {
        'error': e.message
    }, 400

