import pandas as pd


def predict_tag(pipeline, dataset):
    # TODO: IBA SENTENCE JE POVINNA INAK TAM TREBA NADRBAT DEFAULTY
    df = pd.DataFrame(dataset)
    prediction = list(pipeline.predict(df))
    return prediction
