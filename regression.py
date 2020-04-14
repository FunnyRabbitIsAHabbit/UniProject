"""

Uni project

Developer: Stanislav Alexandrovich Ermokhin

"""

from datetime import datetime
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import pandas as pd


from OOP import *


def ecm_model(ts_data_dep, ts_data_indep):
    """

    :param ts_data_dep: pandas.DataFrame
    :param ts_data_indep: pandas.DataFrame
    :return: results string
    """

    results = 'ECM results'

    with open('ECM_model'+str(datetime.now().timestamp())+'.data', 'w') as a:
        a.write(results)

    return results


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


def arima_model(ts_data):
    """

    :param ts_data: array like object
    :return: results string
    """

    p = [0, 1, 2]
    d = [0, 1]
    q = [0, 1, 2]
    results = ARIMA(ts_data, order=evaluate_models(ts_data, p, d, q)).fit().summary()

    with open('ARIMA_model'+str(datetime.now().timestamp())+'.data', 'w') as a:
        a.write(str(results))

    return results
