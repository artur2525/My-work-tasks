import pandas as pd
import numpy as np

def fillna_with_mean(
    df: pd.DataFrame, target: str, group: str
) -> pd.DataFrame:
    '''nan to mean'''
    df_ = df.copy()
    
    df_[target].fillna(np.floor(df_.groupby(group)[target].transform('mean')), inplace = True)

    return df_
