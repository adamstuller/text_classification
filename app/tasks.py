from app import celery
from app.machine_learning.train import train_pipeline, nlp4sk_preprocess
from app.constants import DEFAULT_DATASET
from app.config import config


@celery.task()
def train_pipeline_task( pipeline_name, topic_type):
    train_pipeline( 
        pipeline_name=pipeline_name, 
        topic_type=topic_type,
        dataset_name=config['default_dataset'][topic_type]
        )

@celery.task()
def nlp4sk_preprocess_task(input_dataset_name='banks', output_dataset_name=DEFAULT_DATASET):
    nlp4sk_preprocess(input_dataset_name=input_dataset_name, output_dataset_name=output_dataset_name)