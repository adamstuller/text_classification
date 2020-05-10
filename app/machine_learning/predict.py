import pandas as pd
import numpy as np
from flask import current_app


def predict_tag(pipeline, dataset):
    # TODO: IBA SENTENCE JE POVINNA INAK TAM TREBA NADRBAT DEFAULT
    df = pd.DataFrame(list(dataset))
    if not 'parent_tag' in df:
        df['parent_tag'] = np.nan
    current_app.logger.info(dataset)
    prediction = pipeline.predict(df)
    current_app.logger.info(prediction)
    return list(prediction)
