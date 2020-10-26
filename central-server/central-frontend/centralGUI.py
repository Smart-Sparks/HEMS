# centralGUI.py

# START IMPORTS
import tkinter as tk
from tkinter import ttk

from HomeRepresentation import Home, HomeList, GetAllHomeIDs, HomeTab
import random
import string
import numpy as np
import datetime

import matplotlib.pyplot as plt
# https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
# END IMPORTS

# START CLASSES
# CentralGUI: Class for managing the TKinter Frame that shows the central GUI
class CentralGUI(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("HEMS")
        self.database_file = 'D:\\Documents\\GitRepos\\central-server\\v2\\centralCode\\dbs\\data.db'
        self.output_csv = "D:\\Documents\\GitRepos\\central-server\\v2\\centralCode\\testout.csv"
        # pack into master element
        self.pack()
        # Create notebook for tabbed windows
        self.pages = ttk.Notebook(self)
        self.pages.pack(fill=tk.BOTH, expand=1)
        # When the frame is resized, resize the notebook as well.
        self.bind("<Configure>", self.Scale)
        self.SetupMainPanel()

    # Creates the initial panel the user sees when the app is opened
    def SetupMainPanel(self):
        self.maintab = tk.Frame()

        tk.Label(self.maintab, text="Home Server Selection:").pack()

        # Create list of home servers and put into tab
        self.homeServerListbox = HomeList(self.maintab, selectmode=tk.SINGLE)
        self.homeServerListbox.pack(fill=tk.BOTH, side=tk.LEFT, expand=1)

        # ***********************************************************
        # *** RETRIEVE LIST OF UNIQUE HOME IDs FROM DATABASE HERE ***
        # ***********************************************************
        home_ids = GetAllHomeIDs(self.database_file)
        print(home_ids)
        # Insert representations for each home into the listbox
        for id in home_ids:
            # s is temporary substitute for Home IDs
            # s = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
            home = Home(str(id), self.database_file)
            home.ReadData()
            self.homeServerListbox.insert(tk.END, home)
        #self.PreloadHomeTabs(0)
        # Open tab for home server on double click
        self.homeServerListbox.bind("<Double-Button-1>", self.onHomeSelect)
        # Embed analytics chart in main tab
        # self.EmbedChart(self.maintab, range(3000))
        # Add as first tab to notebook
        self.pages.add(self.maintab, text="Central")

    # Resizes notebook to fill frame when application changes size
    def Scale(self, e):
        self.pages.config(height=self.master.winfo_height(), width=self.master.winfo_width()-10)

    # When user selects a home server, another tab is opened to display info
    def onHomeSelect(self, e):
        # Gets the selection from homeServerListbox
        selection = self.homeServerListbox.curselection()
        value = self.homeServerListbox.get(selection[0])
        # value[0].ReadData()
        self.OpenHomeTab(selection[0])


    # Opens tab of Home at idx of homeServerListbox
    def OpenHomeTab(self, i):
        self.CreateHomeTab(i)


    # Creates new tab to show home server information
    def CreateHomeTab(self, idx):
        # tab = tk.Frame()
        home = self.homeServerListbox.get(idx)[0]

        tab = HomeTab(home, self.pages)

        # # Create list of data related to specific home server
        # box = tk.Listbox(tab, selectmode=tk.SINGLE)
        # box.pack(fill=tk.Y, side=tk.LEFT, expand=0)
        # data = home.GetData() # pandas dataframe
        # energy = home.GetEnergy()
        # for i in energy[0:100]:
        #     box.insert(tk.END, str(i))
        # # Create buttons
        # buttonframe = tk.Frame(tab)
        # export = tk.Button(buttonframe, text="Export Home Data", command=self.ExportHomeData)
        # close = tk.Button(buttonframe, text="Close Tab", command=self.CloseCurrentTab)
        # # export.bind("<Button-1>", self.ExportHomeData)
        # # close.bind("<Button-1>", self.CloseCurrentTab)
        # export.pack(side=tk.LEFT)
        # close.pack(side=tk.RIGHT)
        # buttonframe.pack(side=tk.TOP)
        #
        # # Create date filters
        # filterframe = tk.Frame(tab)
        # filterbutton = tk.Button(filterframe, text="Filter")
        # filterbutton.pack(side=tk.BOTTOM, fill=tk.X, expand=1)
        #
        # today=datetime.date.today()
        # # Start date filters
        # f = tk.Frame(filterframe)
        # ysl = tk.Label(f, text="Start Year")
        # ystart = tk.Entry(f, bd=2)
        # ystart.insert(0, today.year)
        # ysl.pack(side=tk.TOP)
        # ystart.pack(side=tk.BOTTOM)
        # f.pack(side=tk.RIGHT)
        #
        # f = tk.Frame(filterframe)
        # msl = tk.Label(f, text="Start Month")
        # mstart = tk.Entry(f, bd=2)
        # mstart.insert(0, today.month)
        # msl.pack(side=tk.TOP)
        # mstart.pack(side=tk.BOTTOM)
        # f.pack(side=tk.RIGHT)
        #
        # f = tk.Frame(filterframe)
        # dsl = tk.Label(f, text="Start Day")
        # dstart = tk.Entry(f, bd=2)
        # dstart.insert(0, today.day)
        # dsl.pack(side=tk.TOP)
        # dstart.pack(side=tk.BOTTOM)
        # f.pack(side=tk.RIGHT)
        #
        # f = tk.Frame(filterframe)
        # yel = tk.Label(f, text="End Year")
        # yend = tk.Entry(f, bd=2)
        # yend.insert(0, today.year)
        # yel.pack(side=tk.TOP)
        # yend.pack(side=tk.BOTTOM)
        # f.pack(side=tk.RIGHT)
        #
        # f = tk.Frame(filterframe)
        # mel = tk.Label(f, text="End Month")
        # mend = tk.Entry(f, bd=2)
        # mend.insert(0, today.month)
        # mel.pack(side=tk.TOP)
        # mend.pack(side=tk.BOTTOM)
        # f.pack(side=tk.RIGHT)
        #
        # f = tk.Frame(filterframe)
        # dela = tk.Label(f, text="End Day")
        # dend = tk.Entry(f, bd=2)
        # dend.insert(0, today.day)
        # dela.pack(side=tk.TOP)
        # dend.pack(side=tk.BOTTOM)
        # f.pack(side=tk.RIGHT)
        #
        # filterframe.pack(side=tk.BOTTOM)
        #
        # # Embed analytics chart in tab
        # chart = self.EmbedHomeDataChart(tab, home, min(home.GetNumDataPts(), 100))

        # Add tab to notebook
        self.pages.add(tab, text=str(home.GetID()))

        # return tab
        return tab

    # Forget the currently selected tab
    def CloseCurrentTab(self, e=None):
        self.pages.forget(self.pages.select())

    # Creates and packs a matplotlib plot into the given widget component
    def EmbedChart(self, master, data):
        power = np.asarray([float(r[0]) for r in data[0:3000]])

        fig = Figure(figsize=(5, 4), dpi=100)
        t = range(3000)
        ax = fig.add_subplot(111)
        ax.plot(t, power[0:3000])
        ax.axes.yaxis.set_ticks([])

        canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    # Creates and embeds a figure displaying data for specific home server
    def EmbedHomeDataChart(self, master, home, numpts=5):
        power = home.GetPower()
        irms = home.GetIRMS()
        energy = home.GetEnergy()
        powerfactor = home.GetPowerFactor()
        data_amount = home.GetNumDataPts()

        if numpts > 0 and numpts <= data_amount:
            fig = Figure(figsize=(5, 4), dpi=100)
            t = range(numpts)
            # Power
            ax = fig.add_subplot(221)
            ax.plot(t, power[data_amount-numpts:], 'r')
            # ax.axes.yaxis.set_ticks([])
            ax.axes.set_title("Power")
            # Power Factor
            ax = fig.add_subplot(222)
            ax.plot(t, powerfactor[data_amount-numpts:], 'y')
            # ax.axes.yaxis.set_ticks([])
            ax.axes.set_title("Power Factor")
            # Energy
            ax = fig.add_subplot(223)
            ax.plot(t, energy[data_amount-numpts:], 'b')
            # ax.axes.yaxis.set_ticks([])
            ax.axes.set_title("Energy")
            # IRMS
            ax = fig.add_subplot(224)
            ax.plot(t, irms[data_amount-numpts:], 'k')
            # ax.axes.yaxis.set_ticks([])
            ax.axes.set_title("IRMS")

            canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
            return canvas.get_tk_widget()
        return None


    def ExportHomeData(self, e=None):
        # Get tab name
        id = self.pages.tab(self.pages.select(), "text")
        home = self.homeServerListbox.getByID(id)
        home.GetData().to_csv(self.output_csv)
        print(home.GetData())


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x600")
        app = CentralGUI(master=self)
        app.pack()

    def Run(self):
        self.mainloop()
# END CLASSES



def main():
    app = App()
    app.Run()


if __name__ == "__main__":
    main()