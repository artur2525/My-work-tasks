import numpy as np
import pandas as pd

def limit_gmv(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Наша модель динамического ценообразования на маркетплейсе KarpovExpress 
    '''

    df_ = df.copy()
    df_['gmv'] = np.where(np.floor(df_['gmv'] / df_['price']) > df_['stock'],
                         df_['price'] * df_['stock'], df_['gmv'])

    df_['gmv'] = np.where(np.floor(df_['gmv'] / df_['price']) != (df_['gmv'] / df_['price']),
                         np.floor(df_['gmv'] / df_['price']) * df_['price'], df_['gmv'])
    return df_