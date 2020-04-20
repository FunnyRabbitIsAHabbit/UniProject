"""

Uni project

Developer: Stanislav Alexandrovich Ermokhin

"""


import statsmodels.api as sm
import pandas as pd
import statsmodels.formula.api as smf
import pmdarima as pm
import statsmodels.api as sm

from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from datetime import datetime


from OOP import *


def linear_model(name_data, ts_data_dep, ts_data_indep):
    """

    :param name_data: str
    :param ts_data_dep: pandas.DataFrame
    :param ts_data_indep: pandas.DataFrame
    :return: results string
    """

    filename = 'LINEAR_model'+name_data+str(datetime.now().timestamp())+'.txt'

    ts_data_indep['Intercept'] = [1.0 for _ in len(ts_data_dep.index)]
    reg = sm.OLS(ts_data_dep, ts_data_indep)
    model_fit = reg.fit()
    results = model_fit.summary()

    with open(filename, 'w') as a:
        a.write(str(results))

    return filename


def evaluate_arima_model(X, arima_order):
    # prepare training dataset
    train_size = 21//24
    train, test = X[0:train_size], X[train_size:]
    history = [x for x in train]
    # make predictions
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=arima_order)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])
    # calculate out of sample error
    error = mean_squared_error(test, predictions)
    return error


def evaluate_models(dataset, p_values, d_values, q_values):
    best_score, best_cfg = float('inf'), None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p, d, q)
                try:
                    mse = evaluate_arima_model(dataset, order)
                    if mse < best_score:
                        best_score, best_cfg = mse, order
                except Exception:
                    continue
    return best_cfg or (1, 1, 1)


def arima_model(name_data, ts_data, p=None, d=None, q=None):
    """

    :param name_data: str
    :param ts_data: array like object
    :param p: str or None
    :param d: str or None
    :param q: str or None
    :return: results string
    """

    try:
        p = int(p)
        d = int(d)
        q = int(q)

        model_fit = ARIMA(ts_data, order=(p, d, q)).fit()

    except Exception as error:
        print('_ERROR_'*10)
        print(error)

        model_fit = pm.auto_arima(ts_data)

    results = model_fit.summary()
    filename = 'ARIMA_model_'+name_data+str(datetime.now().timestamp())+'.txt'

    with open(filename, 'w') as a:
        a.write(str(results))

    return filename
