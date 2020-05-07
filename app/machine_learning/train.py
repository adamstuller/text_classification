from app.machine_learning.preprocessing import  TFIDFTransformer, LDATransformer, OneHotTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
from app.config import config, PARENT_CLASS_COLUMN_NAME, UPDATED_SENTENCE_COLUMN_NAME
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import RandomOverSampler
from .preprocessing import oversample_strategy, TagBalancer

def train_pipe(X: pd.DataFrame, Y: pd.DataFrame, limit=20, default_tag='Neutral'):

    tb = TagBalancer(limit, default_tag=default_tag)
    Y = tb.fit_transform(Y)

    os = RandomOverSampler(random_state=0, sampling_strategy=oversample_strategy)
    x_resampled, y_resampled = os.fit_resample(X, Y)

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
    

    pipe.fit(x_resampled, y_resampled)
    return pipe
