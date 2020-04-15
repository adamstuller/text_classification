from time import sleep
import requests


class NLP4SKSimplePreprocesser():

    def __init__(self, sentence_column):
        self.sentence_column = sentence_column

    def __preprocess_sentence(self, sentence, dll):
        params = {
            "text": sentence,
            "apikey": "Stuller2020FIIT",
            "lemmatizer": "ProbabilisticLemmatizer",
            "textrestorer": "ProbabilisticDiacriticRestorer"
        }
        response = requests.post(
            "http://arl6.library.sk/nlp4sk/api",
            data=params
        )
        sleep(dll)
        return response.json()

    def __get_lemma(self, token):

        return \
            token['word'] \
            if token['word'] in ['A', '?'] or token['lemma'][0] == '?' \
            else \
            token['lemma'][0]


    def __transform_one(self, sentence, index):

        try:
            processed_comment = self.__preprocess_sentence(
                sentence, 1
            )

            processed_sentence = map(self.__get_lemma, processed_comment)

            print(f'sentence  n. {index} processed')
            return ' '.join(filter(lambda x: x != None, processed_sentence))
        except:
            print(f'error occured on sentence n. {index}')
            return ''

    def fit(self, x, y=None):
        return self

    def transform(self, l: list):
        enriched = map(
            lambda x: {
                'updated_sentence':  self.__transform_one(x[1][self.sentence_column], x[0]),
                **x[1]
            },
            enumerate(l)
        )

        return filter(
            lambda x: not x['updated_sentence'] == '',
            enriched
        )
