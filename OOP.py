"""
OOP part of the program

from GitHub: https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8
"""

import tkinter as tk
from tkinter import Frame, TOP, BOTH
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,\
    NavigationToolbar2Tk
from matplotlib.figure import Figure


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


class VerticalScrolledFrame:
    """
        A vertically scrolled Frame that can be treated like any other Frame
        ie it needs a master and layout and it can be a master.
        :width:, :height:, :bg: are passed to the underlying Canvas
        :bg: and all other keyword arguments are passed to the inner Frame
        note that a widget layed out in this frame will have a self.master 3 layers deep,
        (outer Frame, Canvas, inner Frame) so
        if you subclass this there is no built in way for the children to access it.
        You need to provide the controller separately.
        """

    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = tk.Frame(master, **kwargs)
        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind_all("<Enter>", self._bind_mouse)
        self.canvas.bind_all("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview
        self.inner = tk.Frame(self.canvas, bg=bg)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(0, 0, window=self.inner, anchor='nw')
        self.inner.bind_all("<Configure>", self._on_frame_configure)
        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion=(0, 0, x2, max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")