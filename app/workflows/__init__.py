from .base import workflows_bp
import app.workflows.topic_workflow
import app.workflows.predict_workflow
import app.workflows.errors

def init_app(app):
    app.register_blueprint(workflows_bp)