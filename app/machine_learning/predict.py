import pandas as pd


def predict_tag(pipeline, dataset):
    df = pd.DataFrame(dataset)
    prediction = list(pipeline.predict(df))
    return prediction
