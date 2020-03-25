from preprocessing import NLP4SKPreprocesser, TFIDFTransformer, LDATransformer, OneHotTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
from joblib import dump, load
from os import path
from config import config
from sklearn.ensemble import RandomForestClassifier
from datetime import date

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--dataset-path", "-dp", dest="dataset_path",
                    default=path.join(config['path_to_datasets'], f'banks.csv'))


def get_data(data=None):
    if data == None:
        banks = pd.read_csv(parser.args.path_to_datasets, names=['class', 'sentence', 'likes',
                                                                 'sentiment_percentage', 'post_id', 'posted_by_bank', 'parent_class'])
        banks = banks[banks.sentence.notna()]
        banks['class'] = banks['class'].apply(
            lambda x: x if x != 'Problémy s produktov' else 'Problémy s produktom')
        banks = banks.drop_duplicates(subset='sentence')
        banks.index = range(len(banks))
    else:
        banks = data
    return banks


if __name__ == "__main__":

    pipe = Pipeline(
        steps=[
            ('nlp4sk', NLP4SKPreprocesser('sentence')),
            ('tf-idf', TFIDFTransformer('updated_sentence')),
            ('one-hot', OneHotTransformer(['parent_class'])),
            ('random_forest', RandomForestClassifier(n_estimators=200,
                                                     max_depth=50, criterion='gini', bootstrap=True, random_state=42))
        ],
        verbose=True
    )
    print('fitting')
    pipe.fit(get_data().drop(
        columns=['class']), get_data()['class'])
    dump(pipe, path.join(config['path_to_models'],
                         f"pipeline-{str(date.today())}.joblib"))
