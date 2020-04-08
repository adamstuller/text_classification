import pandas as pd
import numpy as np
from time import sleep
import re
import datetime
from functools import reduce
import requests
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation


SLOVAK_STOPWORDS = ['a',
                    'aby',
                    'aj',
                    'ak',
                    'ako',
                    'ale',
                    'alebo',
                    'and',
                    'ani',
                    'áno',
                    'asi',
                    'až',
                    'bez',
                    'bude',
                    'budem',
                    'budeš',
                    'budeme',
                    'budete',
                    'budú',
                    'by',
                    'bol',
                    'bola',
                    'boli',
                    'bolo',
                    'byť',
                    'cez',
                    'čo',
                    'či',
                    'ďalší',
                    'ďalšia',
                    'ďalšie',
                    'dnes',
                    'do',
                    'ho',
                    'ešte',
                    'for',
                    'i',
                    'ja',
                    'je',
                    'jeho',
                    'jej',
                    'ich',
                    'iba',
                    'iné',
                    'iný',
                    'som',
                    'si',
                    'sme',
                    'sú',
                    'k',
                    'kam',
                    'každý',
                    'každá',
                    'každé',
                    'každí',
                    'kde',
                    'keď',
                    'kto',
                    'ktorá',
                    'ktoré',
                    'ktorou',
                    'ktorý',
                    'ktorí',
                    'ku',
                    'lebo',
                    'len',
                    'ma',
                    'mať',
                    'má',
                    'máte',
                    'medzi',
                    'mi',
                    'mna',
                    'mne',
                    'mnou',
                    'musieť',
                    'môcť',
                    'môj',
                    'môže',
                    'my',
                    'na',
                    'nad',
                    'nám',
                    'náš',
                    'naši',
                    'nie',
                    'nech',
                    'než',
                    'nič',
                    'niektorý',
                    'nové',
                    'nový',
                    'nová',
                    'nové',
                    'noví',
                    'o',
                    'od',
                    'odo',
                    'of',
                    'on',
                    'ona',
                    'ono',
                    'oni',
                    'ony',
                    'po',
                    'pod',
                    'podľa',
                    'pokiaľ',
                    'potom',
                    'práve',
                    'pre',
                    'prečo',
                    'preto',
                    'pretože',
                    'prvý',
                    'prvá',
                    'prvé',
                    'prví',
                    'pred',
                    'predo',
                    'pri',
                    'pýta',
                    's',
                    'sa',
                    'so',
                    'si',
                    'svoje',
                    'svoj',
                    'svojich',
                    'svojím',
                    'svojími',
                    'ta',
                    'tak',
                    'takže',
                    'táto',
                    'teda',
                    'te',
                    'tě',
                    'ten',
                    'tento',
                    'the',
                    'tieto',
                    'tým',
                    'týmto',
                    'tiež',
                    'to',
                    'toto',
                    'toho',
                    'tohoto',
                    'tom',
                    'tomto',
                    'tomuto',
                    'toto',
                    'tu',
                    'tú',
                    'túto',
                    'tvoj',
                    'ty',
                    'tvojími',
                    'už',
                    'v',
                    'vám',
                    'váš',
                    'vaše',
                    'vo',
                    'viac',
                    'však',
                    'všetok',
                    'vy',
                    'z',
                    'za',
                    'zo',
                    'že']


class NLP4SKPreprocesser():

    def __init__(self, sentence_column):
        self.sentence_column = sentence_column

    def __reconstruct_sentence(self, sentence, dll):
        params = {
            "text": sentence,
            "apikey": "Stuller2020FIIT",
            "textrestorer": "ProbabilisticDiacriticRestorer",
        }
        response = requests.post(
            "http://arl6.library.sk/nlp4sk/api", data=params)
        sleep(dll)
        # reduce(lambda acc, x: acc + ' ' + x['word'], response.json(), '')
        return " ".join(list(map(lambda x: x['word'], response.json())))

    def __preprocess_sentence(self, sentence, dll):
        params = {
            "text": sentence,
            "apikey": "Stuller2020FIIT",
            "lemmatizer": "ProbabilisticLemmatizer",
            "postagger": "ProbabilisticPOSTagger",
            "tokenizer": "SmartRuleTokenizer"
        }
        response = requests.post(
            "http://arl6.library.sk/nlp4sk/api", data=params)
        sleep(dll)
        return response.json()

    def __transform_one(self, sentence):

        try:
            restored_sentence = self.__reconstruct_sentence(sentence, 1)
            processed_comment = self.__preprocess_sentence(
                restored_sentence, 1)

            processed_sentence = []
            for x in processed_comment:
                if x['word'] == 'A' or x['word'] == '?':
                    processed_sentence.append(x['word'])
                elif x['lemma'][0] != '?' or x['word'] == '?':
                    processed_sentence.append(x['lemma'][0])
                else:
                    processed_sentence.append(x['word'])

            return ' '.join(filter(lambda x: x != None, processed_sentence))
        except:
            print('error')
            return ''

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        copied_df = x.copy(deep=True)
        updated_sentence = x.sentence.apply(self.__transform_one)
        us = pd.DataFrame(updated_sentence)
        return copied_df.merge(us, left_index=True, right_index=True)\
            .rename(columns={f'{self.sentence_column}_x': self.sentence_column, f'{self.sentence_column}_y': f'updated_{self.sentence_column}'})\
            .drop(columns=[self.sentence_column])


class NLP4SKSimplePreprocesser():

    def __init__(self, sentence_column):
        self.sentence_column = sentence_column

    def __reconstruct_sentence(self, sentence, dll):
        params = {
            "text": sentence,
            "apikey": "Stuller2020FIIT",
            "textrestorer": "ProbabilisticDiacriticRestorer",
        }
        response = requests.post(
            "http://arl6.library.sk/nlp4sk/api", data=params)
        sleep(dll)
        # reduce(lambda acc, x: acc + ' ' + x['word'], response.json(), '')
        return " ".join(list(map(lambda x: x['word'], response.json())))

    def __preprocess_sentence(self, sentence, dll):
        params = {
            "text": sentence,
            "apikey": "Stuller2020FIIT",
            "lemmatizer": "ProbabilisticLemmatizer",
            "postagger": "ProbabilisticPOSTagger",
            "tokenizer": "SmartRuleTokenizer"
        }
        response = requests.post(
            "http://arl6.library.sk/nlp4sk/api", data=params)
        sleep(dll)
        return response.json()

    def __transform_one(self, sentence):

        try:
            restored_sentence = self.__reconstruct_sentence(sentence, 1)
            processed_comment = self.__preprocess_sentence(
                restored_sentence, 1)

            processed_sentence = []
            for x in processed_comment:
                if x['word'] == 'A' or x['word'] == '?':
                    processed_sentence.append(x['word'])
                elif x['lemma'][0] != '?' or x['word'] == '?':
                    processed_sentence.append(x['lemma'][0])
                else:
                    processed_sentence.append(x['word'])

            return ' '.join(filter(lambda x: x != None, processed_sentence))
        except:
            print('error')
            return ''

    def fit(self, x, y=None):
        return self

    def transform(self, l: list):
        return reduce(
            lambda acc, x: {
                **acc,
                **{x['id']: self.__transform_one(x[self.sentence_column])},
            },
            l,
            {}
        )


class TFIDFTransformer():

    def __init__(self, sentence_column):
        self.tfidf = TfidfVectorizer(stop_words=SLOVAK_STOPWORDS,
                                     lowercase=False,
                                     token_pattern=u'(?u)\\b\\w+\\b',
                                     ngram_range=(1, 3),
                                     max_features=500
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


class LDATransformer():
    def __init__(self, topic_sizes: list, word_columns: list):
        self.LDAs = list(map(lambda size: LatentDirichletAllocation(
            n_components=size, random_state=42), topic_sizes))
        self.word_columns = word_columns

    def fit(self, x, y=None):
        for LDA in self.LDAs:
            LDA.fit(x[self.word_columns])
        return self

    def transform(self, x):
        copied_x = x.copy(deep=True)
        for i, LDA in enumerate(self.LDAs):
            topic_results = LDA.transform(copied_x[self.word_columns])
            copied_x[f"topic_{i}"] = topic_results.argmax(axis=1)
        return copied_x


class OneHotTransformer():
    def __init__(self, columns):
        self.columns = columns    # Categorical
        self.all_columns = []     # All columns of trainning data, gets filled in fit method
        # This gets filled while fitting, contains all caegories created by get_dummies on training data
        self.categories = []

    def __update_categories(self, df):
        more_columns = filter(
            lambda x: x not in self.all_columns and x not in self.categories, [*df.columns])
        df = df.drop(columns=more_columns)

        for missing_row in filter(lambda x: x not in [*df.columns], self.categories):
            df[missing_row] = 0
        return df

    def __column_one_hot(self, df, column):
        encoded = pd.get_dummies(df[column], prefix=column)
        # .rename(columns=lambda x: x.lower())
        return pd.merge(df, encoded, left_index=True, right_index=True).drop(columns=column)

    def __get_categories(self, df, column):
        return [*pd.get_dummies(df[column], prefix=column).columns]

    def fit(self, x, y=None):
        self.all_columns = [*x.columns]
        for column in self.columns:
            for cat in self.__get_categories(x, column):
                self.categories.append(cat)
        return self

    def transform(self, x):
        return self.__update_categories(
            reduce(lambda df, column: self.__column_one_hot(
                df, column), self.columns, x)
        )
