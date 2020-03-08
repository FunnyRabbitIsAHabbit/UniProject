"""

Uni project

Developer: Stanislav Alexandrovich Ermokhin

"""

from datetime import datetime


def ecm_model(ts_data):
    """

    :param ts_data: pandas.DataFrame
    :return: results string
    """

    results = 'ECM results'

    with open('ECM_model'+str(datetime.now().timestamp())+'.data', 'w') as a:
        a.write(results)

    return results


def arima_model(ts_data):
    """

    :param ts_data: pandas.DataFrame
    :return: results string
    """

    results = 'ARIMA results'

    with open('ARIMA_model'+str(datetime.now().timestamp())+'.data', 'w') as a:
        a.write(results)

    return results
