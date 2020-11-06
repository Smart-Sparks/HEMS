# centralGUI.py

# START IMPORTS
import tkinter as tk
from tkinter import ttk

from HomeRepresentation import Home, HomeList, GetAllHomeIDs, HomeNotebookTab
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
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=1)
        # Insert representations for each home into the listbox
        if home_ids is not None:
            for id in home_ids:
                home = Home(str(id), self.database_file)
                # Load data from past day
                # home.ReadData()
                home.ReadDataInRange(yesterday, today)
                self.homeServerListbox.insert(tk.END, home)
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
        home = self.homeServerListbox.get(idx)[0]
        tab = HomeNotebookTab(home, self.pages)
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