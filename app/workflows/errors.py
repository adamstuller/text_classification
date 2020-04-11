from .base import workflows_bp
from flask import current_app
from jsonschema import validate, ValidationError, SchemaError 
from werkzeug.exceptions import BadRequest



@workflows_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    current_app.logger.error(e.message)
    return {
        'error': 'Bad Request',
        'message': e.message
    }, 400

@workflows_bp.errorhandler(SchemaError)
def handle_schema_error(e):
    current_app.logger.error(e.message)
    return {
        'error': 'Schema Error',
        'message': e.message
    }, 400

