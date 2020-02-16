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
    N, S, W, E, SUNKEN, RAISED, Checkbutton
# import lxml.html as h
# import aiohttp
# import asyncio
# import pandas as pd
from OOP import *
# from pandas.plotting import register_matplotlib_converters
# from PIL import Image, ImageTk


# register_matplotlib_converters()

DEFAULT_FR_DATE = '31/01/2018'
DEFAULT_TO_DATE = '31/01/2019'
BUTTON_WIDTH = 10

root = Tk()
root.title('Indicator Analyzer')
root.geometry('960x700')
root.resizable(width=True,
               height=True)

top_frame = Frame(root)
top_frame.grid(row=0, column=0)


def load_button_bound(event=None):
    """
    Bound events on Load button

    :param event: Tk event
    :return: None
    """

    global graph_object, photo

    load_button.config(relief=SUNKEN)
    try:
        graph_object.destroy()

        graph_object = PlotWindow(top_frame)
        mpl_subplot = MPLPlot()
        x = np.linspace(0, 2, 100)
        mpl_subplot.build_plot(x, x ** 2, 'x**2')
        mpl_subplot.build_plot(x, x ** 3, 'x**3')
        mpl_subplot.build_plot(x, x, 'x')
        mpl_subplot.suptitle('Plot Title')
        mpl_subplot.nice_plot('x', 'f(x)')
        graph_object.add_mpl_figure(mpl_subplot)

        graph_object.grid(row=4, column=2, columnspan=4, sticky=N)

    except Exception as error:
        commentary_text['text'] = error

    load_button.config(relief=RAISED)


def results_button_bound(event=None):
    """

    :param event: Tk event
    :return: None
    """

    global results_object

    results_button.config(relief=SUNKEN)

    try:
        results_object.destroy()

        results_object = Label(top_frame, text=(str(round(random.random(), 4))*4+'\n')*4)
        results_object.grid(row=5, column=2, columnspan=4, sticky=S)

    except Exception as error:
        commentary_text['text'] = error

    results_button.config(relief=RAISED)


def data_load_button_bound(event=None):
    """
    Bound events on Load Data button

    :param event: Tk event
    :return: None
    """

    global vertical_frame

    data_load_button.config(relief=SUNKEN)

    try:
        vertical_frame.destroy()

        vertical_frame = VerticalScrolledFrame(top_frame,
                                               height=600)
        vertical_frame.grid(row=4, column=0, rowspan=2, columnspan=2)

        for i in range(100):
            text_variable = 'label'*4 + str(int(random.random()*100))
            Checkbutton(vertical_frame,
                        text=text_variable).grid(row=i,
                                                 column=0,
                                                 sticky=W)

    except Exception as error:
        commentary_text['text'] = error

    data_load_button.config(relief=RAISED)


def exit_button_bound(event=None):
    """
    Bound events on Exit button

    :param event: Tk event
    :return: None
    """

    global root

    exit_button.config(relief=SUNKEN)
    root.destroy()

    try:
        exit()

    except KeyboardInterrupt:
        pass


# Buttons -----------------------------------------------------------
exit_button = Button(top_frame,
                     width=BUTTON_WIDTH, text='EXIT',
                     command=exit_button_bound)
exit_button.grid(row=0, column=0, sticky=N+S+E, rowspan=3)
load_button = Button(top_frame,
                     width=BUTTON_WIDTH, text='LOAD\nGRAPH',
                     command=load_button_bound)
load_button.grid(row=0, column=1, sticky=N+S+W, rowspan=3)
results_button = Button(top_frame,
                        width=BUTTON_WIDTH, text='SHOW\nRESULTS',
                        command=results_button_bound)
results_button.grid(row=0, column=4, sticky=N+S+E, rowspan=3)
data_load_button = Button(top_frame,
                          width=BUTTON_WIDTH, text='LOAD\nVARIABLES',
                          command=data_load_button_bound)
data_load_button.grid(row=0, column=5, sticky=N+S+W, rowspan=3)
# -------------------------------------------------------------------

# Frames and Labels -------------------------------------------------
Label(top_frame,
      text='From date: ').grid(row=0, column=2)
Label(top_frame,
      text='To date: ').grid(row=0, column=3)

fr_date = Entry(top_frame)
to_date = Entry(top_frame)

fr_date.insert(0, DEFAULT_FR_DATE)
to_date.insert(0, DEFAULT_TO_DATE)
fr_date.grid(row=1, column=2)
to_date.grid(row=1, column=3)

commentary_text = Label(top_frame, text='Welcome to Indicator Analyzer!\nLet\'s work!')
commentary_text.grid(row=2, column=2, columnspan=2)

vertical_frame = VerticalScrolledFrame(top_frame,
                                       height=600)
vertical_frame.grid(row=4, column=0, rowspan=2, columnspan=2)

graph_object = PlotWindow(top_frame)
graph_object.grid(row=4, column=2, columnspan=4, sticky=N)

results_object = Label(top_frame, text=(str(round(random.random(), 4))*4+'\n')*4)
results_object.grid(row=5, column=2, columnspan=4, sticky=S)
# -------------------------------------------------------------------

root.bind('<Return>', load_button_bound)
root.bind('<Escape>', exit_button_bound)

root.mainloop()


