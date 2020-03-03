"""

Uni project's OOP part

Developer: Stanislav Alexandrovich Ermokhin

"""

import tkinter as tk
from tkinter import Frame, TOP, BOTH
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,\
    NavigationToolbar2Tk
from matplotlib.figure import Figure
import pandas_datareader._utils as pdu
from pandas_datareader import wb
import pandas as pd

import local_en as local


class DataSet:

    current_error = None

    def __init__(self, countries=None,
                 indicators=None, start_year=None, stop_year=None):
        """

        :param countries: lst, optional
        :param indicators: lst, optional
        :param start_year: int, optional
        :param stop_year: int, optional
        """

        properties = self.__class__.set_default()
        self.countries = countries or properties['countries']
        self.indicators = indicators or properties['indicators']
        self.start_year = start_year if start_year and start_year < stop_year else 1995
        self.stop_year = stop_year or 2019

    @staticmethod
    def set_default(countries_filename='countries.txt',
                    indicators_filename='indicators.txt'):
        """

        :param countries_filename: str
        :param indicators_filename: str
        :return: dict
        """

        try:
            with open(countries_filename) as a:
                countries_lst = a.readlines()

            with open(indicators_filename) as a:
                indicators_lst = a.readlines()

            for i in range(len(countries_lst)):
                countries_lst[i] = countries_lst[i].rstrip()
            for j in range(len(indicators_lst)):
                indicators_lst[j] = indicators_lst[j].rstrip()

            return {'countries': countries_lst,
                    'indicators': indicators_lst}

        except FileNotFoundError:
            DataSet.current_error = local.ERROR

            return {'countries': None,
                    'indicators': None}

    def __repr__(self):
        """

        :return: str
        """

        dic = self.__dict__

        return 'WorldBankDataSet object:\n' + \
               '\n'.join([str(key) + ': ' + str(dic[key])
                          for key in dic])

    def get_data_id(self, search_keywords):
        """

        :param search_keywords: list
        :return: list
        """

        start, end = self.start_year, self.stop_year
        search_keywords = search_keywords.split()
        try:
            data = wb.search('|'.join(search_keywords))
            DataSet.data = data

            return data['name'].to_list()

        except Exception as error:
            DataSet.current_error = error

            return pd.DataFrame()

    def get_data(self, indicator_set):
        """

        :param indicator_set: set
        :return: pandas.DataFrame
        """

        try:
            data = DataSet.data
            indicator_set_clean = data.loc[data['name'].isin(indicator_set)]['id'].to_list()
            indicators_ids_data = wb.download(country=self.countries,
                                              indicator=indicator_set_clean,
                                              start=self.start_year, end=self.stop_year)

            DataSet.indicators_ids_data = indicators_ids_data

        except AttributeError as error1:
            DataSet.error = local.ERROR + str(error1)

        except pdu.RemoteDataError as error2:
            DataSet.error = local.ERROR + str(error2)

        return


class PlotWindow(Frame):
    """
    A MatPlotLib window
    """

    def __init__(self, window):
        """
        Class constructor

        :param window: mpl window
        """

        Frame.__init__(self, window)
        self.grid(row=3, columnspan=5)

    def unpack(self):
        """
        Delete window with MPL Figure from Tk window
        """

        self.destroy()

    def add_mpl_figure(self, figure):
        """
        Add MatPlotLib Figure

        :param figure: mpl figure
        :return: None
        """

        self.mpl_canvas = FigureCanvasTkAgg(figure, self)
        self.mpl_canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.mpl_canvas, self)
        self.toolbar.update()

        self.mpl_canvas.get_tk_widget().pack(side=TOP,
                                             fill=BOTH, expand=True)
        self.mpl_canvas._tkcanvas.pack(side=TOP,
                                       fill=BOTH, expand=True)


class MPLPlot(Figure):
    """
    A MatPlotLib figure
    """

    def __init__(self):
        """
        Class constructor
        """

        Figure.__init__(self, dpi=100)
        self.plot = self.add_subplot(111)

    def build_plot(self, plot_x, plot_y, label):
        """
        Add plot on a subplot

        :param plot_x: tuple of x_data
        :param plot_y: tuple of y_data
        :param label: label
        :return:
        """

        self.plot.plot(plot_x, plot_y, label=label)

    def nice_plot(self, x_label=None, y_label=None):
        """
        Make plot look nice

        :param x_label: str
        :param y_label: str
        :return: None
        """

        self.plot.grid(True)
        if x_label and y_label:
            self.plot.set_xlabel(x_label)
            self.plot.set_ylabel(y_label)
        self.plot.legend()
