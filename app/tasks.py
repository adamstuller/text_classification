from app import celery
from app.train import train_pipeline

@celery.task()
def make_file(fname, content):
    with open(fname, "w") as f:
        f.write(content)