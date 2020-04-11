from .base import JSONExceptionHandler

handler = JSONExceptionHandler()

def init_app(app):
    handler.init_app(app)