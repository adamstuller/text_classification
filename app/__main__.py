import app.models
from app import factory
import app
import os  
from app.models import Document


app = factory.create_app(celery=app.celery, db=True)

if __name__ == "__main__":
    app.logger.info('Creating db')
    app.run(host='0.0.0.0', port=os.getenv('FLASK_PORT', 5000))
