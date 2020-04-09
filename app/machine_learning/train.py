from app.machine_learning.preprocessing import NLP4SKPreprocesser, TFIDFTransformer, LDATransformer, OneHotTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
from joblib import dump, load
from os import path, listdir
from os.path import isfile, splitext
from app.config import config, PARENT_CLASS_COLUMN_NAME, UPDATED_SENTENCE_COLUMN_NAME
from sklearn.ensemble import RandomForestClassifier
from datetime import date


def train_pipe(X: pd.DataFrame, Y: pd.DataFrame):
    pipe = Pipeline(
        steps=[
            ('tf-idf', TFIDFTransformer(UPDATED_SENTENCE_COLUMN_NAME)),
            ('one-hot', OneHotTransformer([PARENT_CLASS_COLUMN_NAME])),
            (
                'random_forest',
                RandomForestClassifier(
                    n_estimators=200,
                    max_depth=50,
                    criterion='gini',
                    bootstrap=True,
                    random_state=42
                )
            )
        ],
        verbose=True
    )
    

    pipe.fit(X, Y)
    return pipe
