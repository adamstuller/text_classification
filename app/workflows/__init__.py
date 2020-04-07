from .base import workflows_bp
import app.workflows.create_topic

def init_app(app):
    app.register_blueprint(workflows_bp)