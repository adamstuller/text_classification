from flask import jsonify, current_app
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException


class JSONExceptionHandler(object):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def std_handler(self, error):
        # current_app.logger.info(error)
        response = jsonify({
            'error': error.name,
            'message': error.description
        })
        response.status_code = error.code if isinstance(
            error, HTTPException) else 500
        return response

    def init_app(self, app):
        self.app = app
        self.register(HTTPException)
        for code, v in default_exceptions.items():
            self.register(code)

    def register(self, exception_or_code, handler=None):
        self.app.errorhandler(exception_or_code)(handler or self.std_handler)
