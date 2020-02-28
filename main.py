"""

Uni project

Developer: Stanislav Alexandrovich Ermokhin

"""

# import os
import random
import numpy as np
# from datetime import datetime as dt
# from operator import itemgetter
from tkinter import Tk, Label, Frame, Entry, Button, \
    N, S, W, E, SUNKEN, RAISED, MULTIPLE, SINGLE, Listbox, END
# import lxml.html as h
# import aiohttp
# import asyncio
# import pandas as pd
from OOP import *
import local_en as local
# from pandas.plotting import register_matplotlib_converters
# from PIL import Image, ImageTk


# register_matplotlib_converters()

DEFAULT_FR_DATE = '31/01/2018'
DEFAULT_TO_DATE = '31/01/2019'
DEFAULT_KEYWORDS = local.DEFAULT_KEYWORDS
BUTTON_WIDTH = 10
ELEMENTS_IN_LIST = 29
LIST_WIDTH = 29

root = Tk()
root.title(local.ROOT_TITLE)
root.geometry('910x710')
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


def load_button_bound(event=None):
    """
    Bound events on Load button

    :param event: Tk event
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
        mpl_subplot.suptitle('Plot Title')
        mpl_subplot.nice_plot('x', 'f(x)')
        graph_object.add_mpl_figure(mpl_subplot)

        graph_object.grid(row=0, column=0, columnspan=5, sticky=N)

    except Exception as error:
        message_object['text'] = error

    load_button.config(relief=RAISED)


def results_button_bound(event=None):
    """

    :param event: Tk event
    :return: None
    """

    global results_object, message_object

    results_button.config(relief=SUNKEN)

    try:
        results_object.destroy()
        del results_object

        results_object = Label(bottom_frame, text=(str(round(random.random(), 4))*4+'\n')*4)
        results_object.grid(row=0, column=0, columnspan=7, sticky=S)

    except Exception as error:
        message_object['text'] = error

    results_button.config(relief=RAISED)


def data_load_button_bound(event=None):
    """
    Bound events on Load Data button

    :param event: Tk event
    :return: None
    """

    global left_frame, keyword_text,\
        listbox, message_object

    data_load_button.config(relief=SUNKEN)

    try:
        listbox.delete(0, END)

        data_wb = DataSet().get_data(keyword_text.get())

        for data_item in data_wb:
            listbox.insert(END, data_item)

    except Exception as error:
        message_object['text'] = error

    data_load_button.config(relief=RAISED)


def enter_variables_button_bound(event=None):
    """

    :param event: Tk event
    :return: None
    """

    global enter_variables_button,\
        listbox, chosen_variables,\
        dependent_variable

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

        global dependent_variable

        try:
            dependent_variable = inner_listbox.get(inner_listbox.curselection()[0])

        except IndexError:
            pass

    def exit_small(event1=None):
        """

        :param event1: Tk event
        :return: None
        """

        nonlocal master

        exit_button.config(relief=SUNKEN)
        master.destroy()
        del master

    Button(master, text=local.EXIT, command=exit_small).grid(row=0, column=0)
    Button(master, text=local.BUTTON_SELECT, command=get_selected).grid(row=0, column=1)
    Label(master, text=local.DEPENDENT_VARIABLE_SELECTION).grid(row=1, column=0, columnspan=2)
    inner_listbox = Listbox(master, selectmode=SINGLE, width=LIST_WIDTH, height=ELEMENTS_IN_LIST)
    inner_listbox.grid(row=2, column=0, columnspan=2)

    for item in chosen_variables:
        inner_listbox.insert(END, item)

    chosen_variables.clear()

    master.mainloop()

    enter_variables_button.config(relief=RAISED)


def exit_button_bound(event=None):
    """
    Bound events on Exit button

    :param event: Tk event
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

    finally:
        exit()


# Buttons -----------------------------------------------------------
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

keyword_text = Entry(top_frame, width=LIST_WIDTH+10)
keyword_text.insert(0, DEFAULT_KEYWORDS)
keyword_text.grid(row=2, column=2, columnspan=2)

Label(left_frame,
      text=local.ANALYZE_VARIABLES).grid(row=0, column=0, columnspan=2)

listbox = Listbox(left_frame, height=ELEMENTS_IN_LIST, width=LIST_WIDTH,
                  selectmode=MULTIPLE)
listbox.grid(row=1, column=0, columnspan=2)
listbox.insert(END, local.PUSH_LOAD_VARIABLES)

graph_object = PlotWindow(right_frame)
graph_object.grid(row=0, column=0, columnspan=5, sticky=N)

results_object = Label(bottom_frame, text=(str(round(random.random(), 4))*4+'\n')*4)
results_object.grid(row=0, column=2, columnspan=5)
message_object = Label(bottom_frame, text=local.WELCOME)
message_object.grid(row=1, column=0, columnspan=8)

# -------------------------------------------------------------------

root.bind('<Return>', load_button_bound)
root.bind('<Escape>', exit_button_bound)

root.mainloop()
