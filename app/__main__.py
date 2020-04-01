from app import factory
import app
import os

app = factory.create_app(celery=app.celery)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('FLASK_PORT', 5000))

