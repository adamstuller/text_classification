import sys
from sklearn.metrics import confusion_matrix
from joblib import dump, load
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import os

def train(model, x_train, y_train):
    """
    Trains classifier from given model
    :param model: Model to be trained on given data
    :param x_train: Train dataset
    :param y_train: Labels
    :return:
    trained classifier
    """

    model.fit(x_train, y_train)
    return model


def test(classifier, x_test, y_test):
    """
    Tests given trained classfier on given test dataset
    :param classifier: trained classifier
    :param x_test: test dataset
    :param y_test: test labels
    :return: numpy.array, int, int
    confusion matrix of classifier, accuracy rate and error rate
    """

    y_pred = classifier.predict(x_test)

    matrix = confusion_matrix(y_test, y_pred)
    score = classifier.score(x_test, y_test)
    error_rate = 1 - score

    return matrix, score, error_rate


def save(classifier, name):
    """
    Saves classifier into specified folder
    :param classifier: trained classifier to be saved
    :param name: name of the folder in ./data/classifiers into which clf is to be saved
    """
    working_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    CLF_PATH = os.path.join(working_dir,'data', 'models', f"{name}.joblib")
    dump(classifier, CLF_PATH)


def load_clf(name):
    """
    loads classifier
    :param name: name of the folder from where classifier is to be loaded in ./data/classifiers
    :return:
    """
    working_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    CLF_PATH = os.path.join(working_dir,'data', 'models', f"{name}.joblib")
    try:
        return load(CLF_PATH)
    except FileNotFoundError:
        print('No such model exists')
        raise FileNotFoundError


def transform_comments( df, vectorizer ):
    df = df[ ~(df.isnull().sentence == True)].drop_duplicates('sentence')
    x_train, x_test, y_train, y_test = get_train_test(df) 
    vectorizer.fit(x_train)
    x_train = vectorizer.transform(x_train)
    x_test  = vectorizer.transform(x_test)
    return x_train, x_test, y_train, y_test

def predict( model , messages, vectorizer):
    message_series = pd.Series(messages)
    return model.predict(vectorizer.transform(message_series))

def get_train_test( df ):
    x_trains, x_tests,  y_trains, y_tests = [], [], [], []
    for tag in df['class'].unique().tolist():
        x, y = df[df['class'] == tag].sentence, df[df['class'] == tag]['class']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15, random_state=1000)
        x_trains.append(x_train)
        x_tests.append(x_test)    
        y_trains.append(y_train)    
        y_tests.append(y_test)   

    return  pd.concat(x_trains), pd.concat(x_tests), pd.concat(y_trains), pd.concat(y_tests)





def main():
    vectorizer = None
    model = None
    try:
        model = load_clf('LogisticRegression')
        vectorizer = load_clf('Vectorizer')
    except:
        working_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        vectorizer = CountVectorizer()
        df = pd.read_csv(os.path.join(working_dir, 'data', 'labeled_comments.csv'), names=['sentence', 'class'])
        print(df.head())
        x_train, x_test, y_train, y_test = transform_comments(df, vectorizer)
        classifier = LogisticRegression(solver='lbfgs')
        model = train(classifier, x_train, y_train)
        save(model, 'LogisticRegression')
        save(vectorizer, 'Vectorizer')

    messages = sys.argv[1:]
    print(predict(model, messages, vectorizer))

if __name__ == "__main__":
    main()

sys.stdout.flush()

