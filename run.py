from app import factory
import app
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    app = factory.create_app(celery=app.celery)
    app.run()

