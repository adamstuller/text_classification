from app.preprocessing import NLP4SKPreprocesser, TFIDFTransformer, LDATransformer, OneHotTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
from joblib import dump, load
from os import path, listdir
from os.path import isfile, splitext
from app.config import config
from sklearn.ensemble import RandomForestClassifier
from datetime import date
from app.constants import DATASET_ARG, PIPELINE_ARG

import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-path", "-dp", dest="dataset_path",
                        default=path.join(config['path_to_datasets'], f'banks.csv'))
    return parser.parse_args()


def get_data(data=None, path_to_dataset=path.join(config['path_to_datasets'], 'banks.csv')):
    if data == None:
        banks = pd.read_csv(path_to_dataset, names=['class', 'sentence', 'likes',
                                                    'sentiment_percentage', 'post_id', 'posted_by_bank', 'parent_class'])
        banks = banks[banks.sentence.notna()]
        banks['class'] = banks['class'].apply(
            lambda x: x if x != 'Problémy s produktov' else 'Problémy s produktom')
        banks = banks.drop_duplicates(subset='sentence')
        banks.index = range(len(banks))
    else:
        banks = data
    return banks.head(20)


def train_pipeline(dataset_name='banks', pipeline_name=None):

    path_to_pipeline = path.join(
        config['path_to_models'],
        f'{pipeline_name}.joblib' if pipeline_name != None
        else f'pipeline-{str(date.today())}.joblib')
    path_to_dataset = path.join(
        config['path_to_datasets'],
        f'{dataset_name}.csv')

    if not isfile(path_to_dataset):
        raise FileNotFoundError(
            'Dataset stated in dataset_name does not exists'
            )

    pipe = Pipeline(
        steps=[
            ('nlp4sk', NLP4SKPreprocesser('sentence')),
            ('tf-idf', TFIDFTransformer('updated_sentence')),
            ('one-hot', OneHotTransformer(['parent_class'])),
            ('random_forest', RandomForestClassifier(n_estimators=200,
                                                     max_depth=50,
                                                     criterion='gini',
                                                     bootstrap=True,
                                                     random_state=42))
        ],
        verbose=True
    )

    pipe.fit(
        get_data(data=None, path_to_dataset=path_to_dataset)
        .drop(columns=['class']),
        get_data(data=None, path_to_dataset=path_to_dataset)['class']
    )

    dump(pipe, path_to_pipeline)


def get_all(folder_type):

    if folder_type == DATASET_ARG:
        path_to_pipelines = config['path_to_datasets']
    elif folder_type == PIPELINE_ARG:
        path_to_pipelines = config['path_to_models']
    else:
        raise KeyError(
            f'folder_type argument is either "{DATASET_ARG}" or "{PIPELINE_ARG}"'
        )

    files_in_model_dir = list(
        filter(
            lambda f: isfile(path.join(path_to_pipelines, f)),
            listdir(path_to_pipelines)
        )
    )
    return list(
        map(
            lambda f: splitext(f)[0],
            files_in_model_dir
        )
    )


if __name__ == "__main__":
    # args = parse_arguments()
    print(get_all('pipelines'))
    # train_pipeline(args.dataset_path)
