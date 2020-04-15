from sklearn.decomposition import LatentDirichletAllocation

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