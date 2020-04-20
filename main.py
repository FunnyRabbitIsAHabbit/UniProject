"""

Uni project. Main module.

Developer: Stanislav Alexandrovich Ermokhin

"""

import numpy as np
# import lxml.html as h
# import aiohttp
# import asyncio
# import pandas as pd
# import os
# import random

# from datetime import datetime as dt
# from operator import itemgetter
from tkinter import Tk, Label, Frame, Entry, Button, \
    N, S, W, E, SUNKEN, RAISED, MULTIPLE, SINGLE, Listbox,\
    END, Radiobutton, StringVar


from OOP import *
import regression
import local_en as local
# from pandas.plotting import register_matplotlib_converters
# from PIL import Image, ImageTk


# register_matplotlib_converters()

DEFAULT_FR_DATE = '1995'
DEFAULT_TO_DATE = '2020'
DEFAULT_KEYWORDS = local.DEFAULT_KEYWORDS
DEFAULT_p = local.P
DEFAULT_d = DEFAULT_p
DEFAULT_q = DEFAULT_p
BUTTON_WIDTH = 10
ELEMENTS_IN_LIST = 29
LIST_WIDTH = 29

root = Tk()
root.title(local.ROOT_TITLE)
root.geometry('927x710')
root.resizable(width=True,
               height=True)

top_frame = Frame(root)
top_frame.grid(row=0, column=0, columnspan=8, sticky=E)

left_frame = Frame(root)
left_frame.grid(row=1, column=0, columnspan=3, sticky=W)

right_frame = Frame(root)
right_frame.grid(row=1, column=3, columnspan=6, sticky=E)

bottom_frame = Frame(root, height=100)
bottom_frame.grid(row=2, column=0, columnspan=8, sticky=S)
chosen_variables = set()
dependent_variable = ''
model_to_use = ''
regression_results = ''
results_object = 'filename'


def load_button_bound(event=None):
    """
    Bound events on Load button

    :param event: Tk event, optional
    :return: None
    """

    global graph_object, mpl_subplot, message_object

    load_button.config(relief=SUNKEN)

    try:
        try:
            del mpl_subplot

        except NameError:
            pass

        graph_object.destroy()
        del graph_object

        graph_object = PlotWindow(right_frame)
        mpl_subplot = MPLPlot()
        x = np.linspace(0, 2, 100)
        mpl_subplot.build_plot(x, x ** 2, 'x**2')
        mpl_subplot.build_plot(x, x ** 3, 'x**3')
        mpl_subplot.build_plot(x, x, 'x')
        mpl_subplot.suptitle(dependent_variable)
        mpl_subplot.nice_plot('time', dependent_variable)
        graph_object.add_mpl_figure(mpl_subplot)

        graph_object.grid(row=0, column=0, columnspan=5, sticky=N)

    except Exception as error:
        message_object['text'] = error

    load_button.config(relief=RAISED)


def model_bound(event=None):
    """

    :param event: Tk event, optional
    :return: None
    """

    global model_to_use, dependent_variable, chosen_variables

    model_to_use = model_var.get()


def results_button_bound(event=None):
    """

    :param event: Tk event, optional
    :return: None
    """

    global message_object, regression_results

    results_button.config(relief=SUNKEN)

    try:
        new_window = Tk()
        new_window.title(regression_results)

        with open(regression_results) as a:
            lbl = Label(new_window, text=a.read())
        lbl.pack()

        new_window.mainloop()

    except Exception as error:
        message_object['text'] = error

    results_button.config(relief=RAISED)


def data_load_button_bound(event=None):
    """
    Bound events on Load Data button

    :param event: Tk event, optional
    :return: None
    """

    global left_frame, keyword_text,\
        listbox, message_object, wb_data

    data_load_button.config(relief=SUNKEN)
    message_object['text'] = local.WELCOME

    try:
        listbox.delete(0, END)

        wb_data = DataSet(start_year=fr_date.get(), stop_year=to_date.get())
        data_wb = wb_data.get_data_id(keyword_text.get())

        class_error = wb_data.current_error
        if class_error:
            message_object['text'] = class_error

        for data_item in data_wb:
            listbox.insert(END, data_item)

    except Exception as error:
        message_object['text'] = error

    data_load_button.config(relief=RAISED)


def enter_variables_button_bound(event=None):
    """

    :param event: Tk event, optional
    :return: None
    """

    global enter_variables_button,\
        listbox, chosen_variables,\
        dependent_variable, results_object, regression_results

    enter_variables_button.config(relief=SUNKEN)

    for item in listbox.curselection():
        chosen_variables.add(listbox.get(item))

    master = Tk()
    master.title(local.NEW_TITLE)

    def get_selected(event1=None):
        """

        :param event1: Tk event
        :return: None
        """

        global dependent_variable, chosen_variables,\
            wb_data, regression_results

        try:
            dependent_variable = inner_listbox.get(inner_listbox.curselection()[0])
            exit_small()

            try:
                data = wb_data.get_data(chosen_variables)
                data = data[(wb_data.get_id_by_name([dependent_variable])[0])].fillna(method='bfill')
                data = data.iloc[::-1]
                wb_data.current_dep_data = data

                if model_to_use == 'ARIMA':
                    ar_p = p.get()
                    int_d = d.get()
                    ma_q = q.get()
                    regression_results = regression.arima_model(dependent_variable, data, ar_p, int_d, ma_q)
                    message_object['text'] = local.PUSH_RESULTS

                    chosen_variables.clear()

                elif model_to_use == 'LINEAR':
                    indep_data = pd.DataFrame()
                    for var in chosen_variables:
                        independent_data = data[(wb_data.get_id_by_name([var])[0])].fillna(method='bfill')
                        independent_data = independent_data.iloc[::-1]
                        indep_data[var] = independent_data

                    wb_data.current_indep_data = indep_data
                    regression_results = regression.linear_model(dependent_variable, data, indep_data)
                    chosen_variables.clear()

                else:
                    message_object['text'] = local.NO_MODEL_CHOSEN

            except Exception as error:
                message_object['text'] = local.ERROR_INDICATOR_NOT_FOUND + ':\n' + str(error)
                chosen_variables.clear()

        except IndexError:
            chosen_variables.clear()

    def exit_small(event1=None):
        """

        :param event1: Tk event
        :return: None
        """

        nonlocal master

        exit_button.config(relief=SUNKEN)
        master.destroy()

        del master

    def del_listbox_item(event=None):
        """

        :param event: Tk event
        :return: None
        """

        inner_listbox.delete(inner_listbox.curselection())

    Button(master, text=local.EXIT, command=exit_small).grid(row=0, column=0)
    Button(master, text=local.BUTTON_SELECT, command=get_selected).grid(row=0, column=1)
    Label(master, text=local.DEPENDENT_VARIABLE_SELECTION).grid(row=1, column=0, columnspan=2)
    inner_listbox = Listbox(master, selectmode=SINGLE, width=LIST_WIDTH, height=ELEMENTS_IN_LIST)
    inner_listbox.grid(row=2, column=0, columnspan=2)
    inner_listbox.bind('<BackSpace>', del_listbox_item)

    for item in chosen_variables:
        inner_listbox.insert(END, item)

    master.bind('<Return>', get_selected)
    master.mainloop()

    enter_variables_button.config(relief=RAISED)


def exit_button_bound(event=None):
    """
    Bound events on Exit button

    :param event: Tk event, optional
    :return: None
    """

    global root

    exit_button.config(relief=SUNKEN)
    root.destroy()
    del root

    try:
        exit()

    except KeyboardInterrupt:
        pass


# Buttons and Radiobuttons ------------------------------------------
exit_button = Button(top_frame,
                     width=BUTTON_WIDTH, height=int(BUTTON_WIDTH/2),
                     text=local.EXIT,
                     command=exit_button_bound)
exit_button.grid(row=0, column=0, sticky=N+E, rowspan=3)

load_button = Button(top_frame,
                     width=BUTTON_WIDTH, height=int(BUTTON_WIDTH/2),
                     text=local.LOAD_GRAPH,
                     command=load_button_bound)
load_button.grid(row=0, column=1, sticky=N+E, rowspan=3)

results_button = Button(top_frame,
                        width=BUTTON_WIDTH, height=int(BUTTON_WIDTH/2),
                        text=local.SHOW_RESULTS,
                        command=results_button_bound)
results_button.grid(row=0, column=4, sticky=N+W, rowspan=3)

data_load_button = Button(top_frame,
                          width=BUTTON_WIDTH, height=int(BUTTON_WIDTH/2),
                          text=local.LOAD_VARIABLES,
                          command=data_load_button_bound)
data_load_button.grid(row=0, column=5, sticky=N+W, rowspan=3)

enter_variables_button = Button(top_frame,
                                width=BUTTON_WIDTH, height=int(BUTTON_WIDTH/2),
                                text=local.ENTER_VARIABLES,
                                command=enter_variables_button_bound)
enter_variables_button.grid(row=0, column=6, sticky=N+W, rowspan=3)

model_var = StringVar()
ecm_model_button = Radiobutton(master=top_frame, indicatoron=0,
                               text='LINEAR', variable=model_var,
                               value='LINEAR', command=model_bound)
arima_model_button = Radiobutton(master=top_frame, indicatoron=0,
                                 text='ARIMA', variable=model_var,
                                 value='ARIMA', command=model_bound)
ecm_model_button.grid(row=1, column=7, sticky=W)
arima_model_button.grid(row=2, column=7, sticky=W)

# -------------------------------------------------------------------


# Frames and Labels -------------------------------------------------
Label(top_frame,
      text=local.FROM_DATE).grid(row=0, column=2)
Label(top_frame,
      text=local.TO_DATE).grid(row=0, column=3)

fr_date = Entry(top_frame)
to_date = Entry(top_frame)

fr_date.insert(0, DEFAULT_FR_DATE)
to_date.insert(0, DEFAULT_TO_DATE)
fr_date.grid(row=1, column=2)
to_date.grid(row=1, column=3)

p = Entry(bottom_frame)
d = Entry(bottom_frame)
q = Entry(bottom_frame)

p.grid(row=0, column=1)
d.grid(row=0, column=3)
q.grid(row=0, column=5)

pl = Label(bottom_frame, text=local.AUTO_REGRESSION)
dl = Label(bottom_frame, text=local.INTEGRATED)
ql = Label(bottom_frame, text=local.MOV_A)

pl.grid(row=0, column=0)
dl.grid(row=0, column=2)
ql.grid(row=0, column=4)

p.insert(0, DEFAULT_p)
d.insert(0, DEFAULT_d)
q.insert(0, DEFAULT_q)

forecast = Entry(bottom_frame)
forecast_label = Label(bottom_frame, text=local.PROJECTION_PERIOD)

forecast_label.grid(row=1, column=0)
forecast.grid(row=1, column=1)

keyword_text = Entry(top_frame, width=LIST_WIDTH+10)
keyword_text.insert(0, DEFAULT_KEYWORDS)
keyword_text.grid(row=2, column=2, columnspan=2)

Label(left_frame,
      text=local.ANALYZE_VARIABLES).grid(row=0, column=0, columnspan=2)

listbox = Listbox(left_frame, height=ELEMENTS_IN_LIST, width=LIST_WIDTH,
                  selectmode=MULTIPLE)
listbox.grid(row=1, column=0, columnspan=2)

graph_object = PlotWindow(right_frame)
graph_object.grid(row=0, column=0, columnspan=5, sticky=N)


message_object = Label(bottom_frame, text=(local.WELCOME+' '+local.PUSH_LOAD_VARIABLES))
message_object.grid(row=2, column=0, columnspan=8)

Label(top_frame, text=local.MODEL).grid(row=0, column=7, sticky=W)

# -------------------------------------------------------------------

listbox.bind('<Return>', enter_variables_button_bound)
root.bind('<Escape>', exit_button_bound)

root.mainloop()
