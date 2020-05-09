import pandas as pd
import numpy as np


def predict_tag(pipeline, dataset):
    # TODO: IBA SENTENCE JE POVINNA INAK TAM TREBA NADRBAT DEFAULT
    df = pd.DataFrame(dataset)
    if not 'parent_tag' in df:
        df['parent_tag'] = np.nan
    prediction = list(pipeline.predict(df))
    return prediction
