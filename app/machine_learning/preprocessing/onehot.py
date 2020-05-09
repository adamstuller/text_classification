from functools import reduce
import pandas as pd


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
            reduce(
                lambda df, column: self.__column_one_hot(df, column),
                self.columns,
                x
            )
        )
