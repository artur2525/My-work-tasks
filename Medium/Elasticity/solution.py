import pandas as pd
import numpy as np

def elasticity_df(df: pd.DataFrame) -> pd.DataFrame:
    '''elastic count'''
    data = df.copy()
    def lin_reg(prices, qty):
        # Вычисление логарифмов продаж и цен
   
        # Преобразуйте цены и продажи в массивы numpy
        X = np.array(prices)  # Цены
        y = np.log(qty.values + 1)  # Логарифм продаж

        # Рассчитываем коэффициенты линейной регрессии
        X_mean = np.mean(X)
        y_mean = np.mean(y)

        numerator = np.sum((X - X_mean) * (y - y_mean))
        denominator = np.sum((X - X_mean) ** 2)

        # Коэффициенты регрессии
        slope = numerator / denominator
        

        intercept = y_mean - slope * X_mean

        # Предсказание модели
        predicted_Y = slope * X + intercept

        # Рассчитайте коэффициент детерминации (R^2)
        ss_total = np.sum((y - y_mean) ** 2)
        ss_residual = np.sum((y - predicted_Y) ** 2)
        r2_coef = 1 - (ss_residual / ss_total)

        return r2_coef

    data = data.groupby(['sku'])['price', 'qty'].apply(lambda x: lin_reg(x['price'],
                                            x['qty'])).reset_index(name='elasticity')

    return data
