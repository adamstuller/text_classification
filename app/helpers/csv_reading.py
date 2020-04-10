import pandas as pd

def process_csv(csv, column_names: str) -> pd.DataFrame: 
    if not column_names == None:
        return pd.read_csv(csv, names=column_names)
    else:
        return pd.read_csv(csv, index_col=0)