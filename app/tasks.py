from app import celery
from app.machine_learning.train import train_pipeline

@celery.task()
def train_pipeline_task(dataset_name, pipeline_name):
    train_pipeline(dataset_name, pipeline_name)