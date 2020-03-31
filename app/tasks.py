from app import celery
from app.machine_learning.train import train_pipeline, nlp4sk_preprocess
from app.constants import DEFAULT_DATASET


@celery.task()
def train_pipeline_task( pipeline_name):
    train_pipeline( pipeline_name=pipeline_name)

@celery.task()
def nlp4sk_preprocess_task(input_dataset_name='banks', output_dataset_name=DEFAULT_DATASET):
    nlp4sk_preprocess(input_dataset_name=input_dataset_name, output_dataset_name=output_dataset_name)