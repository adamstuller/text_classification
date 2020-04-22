from sklearn.feature_extraction.text import TfidfVectorizer
from .stopwords import SLOVAK_STOPWORDS
import pandas as pd


class TFIDFTransformer():

    def __init__(self, sentence_column):
        self.tfidf = TfidfVectorizer(stop_words=SLOVAK_STOPWORDS,
                                     lowercase=False,
                                     token_pattern=u'(?u)\\b\\w+\\b',
                                     ngram_range=(1, 3),
                                     max_features=50
                                     )
        self.sentence_column = sentence_column

    def fit(self, x, y=None):
        self.tfidf.fit(x[self.sentence_column])
        return self

    def transform(self, x):
        transformed = pd.DataFrame(self.tfidf.transform(x[self.sentence_column]).toarray())\
                        .rename(columns=lambda x: self.tfidf.get_feature_names()[x])
        x.index = transformed.index
        return x.merge(transformed, left_index=True, right_index=True)\
            .drop(columns=[self.sentence_column], errors='ignore')