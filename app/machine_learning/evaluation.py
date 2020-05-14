from sklearn.metrics import f1_score, precision_score, recall_score,  accuracy_score
from sklearn.model_selection import train_test_split
import pandas as pd
from app.machine_learning.train import train_pipe
from app.config import config
from flask import current_app
from app.machine_learning.preprocessing import TagBalancer

def calculate_results(y_test, y_pred):
    return {
        'f1_macro': f1_score(y_test, y_pred, average='macro'),
        'f1_weighted': f1_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='macro'),
        'precision': precision_score(y_test, y_pred, average='macro'),
        'accuracy': accuracy_score(y_test, y_pred)
    }


def get_train_test(x, y, test_size=0.15, drop_classes=[]):
    x_trains, x_tests,  y_trains, y_tests = [], [], [], []
    for tag in y.unique().tolist():
    
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=test_size, random_state=1000)
        x_trains.append(x_train)
        x_tests.append(x_test)
        y_trains.append(y_train)
        y_tests.append(y_test)

    x_train = pd.concat(x_trains)

    return pd.concat(x_trains), pd.concat(x_tests), pd.concat(y_trains), pd.concat(y_tests)


def evaluate(X: pd.DataFrame, Y: pd.DataFrame):
    tb = TagBalancer(config['limit_tag_size'])
    Y = tb.fit_transform(Y)

    test_size = 0.15

    x_train, x_test, y_train, y_test = get_train_test(X, Y, test_size=test_size)
    current_app.logger.info(x_train)
    limit = int(config['limit_tag_size'] * (1 - test_size))
    pipe = train_pipe(x_train, y_train, limit=limit)
    y_pred = pipe.predict(x_test)
    return calculate_results(y_test,  y_pred)
