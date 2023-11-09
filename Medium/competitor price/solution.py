import numpy as np
import pandas as pd


def agg_comp_price(X: pd.DataFrame) -> pd.DataFrame:
    '''pipline for price'''
    x = X.copy()
    if (np.unique(x['agg']) != 'rnk').all():
        x_rnk = x[x['agg'] == 'rnk']
        x = x[x['agg'] != 'rnk']
        agreg = x.groupby(['sku'])['agg'].unique().apply(
            lambda x: ''.join(x)).values
        agreg[agreg == 'med'] = 'median'
        agreg[agreg == 'avg'] = 'mean'
        x_rnk = x_rnk[x_rnk['agg'] == 'rnk'].\
            groupby(['sku', 'agg', 'base_price'])['rank', 'comp_price'].min().\
            reset_index()

        prices = np.diag(x.groupby(['sku', 'agg']).agg(
            {'comp_price': agreg}).values)

        data = x.groupby(['sku', 'agg'])['base_price'].mean().reset_index()

        data['comp_price'] = prices
        data = pd.concat([data, x_rnk.drop('rank', axis=1)], axis=0).sort_values(by='sku').\
            reset_index(drop=True)
        data['new_price'] = np.where(abs(((100 / data['base_price']) * data['comp_price']) - 100) >= 20,
                                     data['base_price'], data['comp_price'])
        data['new_price'].fillna(data['base_price'], inplace=True)

        return data

    elif (np.unique(x['agg']) == 'rnk').all():
        x['rank'].fillna(-1, inplace = True)
        data = x[x['rank'].isin([-1, 0])]
        data = data.drop('rank', axis=1).reset_index(drop = True)
        data['new_price'] = np.where(abs(((100 / data['base_price']) * data['comp_price']) - 100) >= 20,
                                     data['base_price'], data['comp_price'])
        data['new_price'].fillna(data['base_price'], inplace=True)
        return data

    else:
        data = x.groupby(['sku', 'agg', 'base_price'])['rank', 'comp_price'].min().\
            reset_index()

        data = data.drop('rank', axis=1)
        data['new_price'] = np.where(abs(((100 / data['base_price']) * data['comp_price']) - 100) >= 20,
                                     data['base_price'], data['comp_price'])
        data['new_price'].fillna(data['base_price'], inplace=True)
        return data