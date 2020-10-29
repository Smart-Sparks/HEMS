# HomeRepresentation.py

# START IMPORTS
import tkinter as tk

from tkinter import ttk

import numpy as np

import sqlite3
import os
import datetime
import pandas
import csv


import matplotlib.pyplot as plt
# https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
# END IMPORTS

# START METHODS
def GetAllHomeIDs(dbfile):
    if os.path.exists(dbfile):
        try:
            # Open connection with SQLite db
            con = sqlite3.connect(dbfile)
            cur = con.cursor()
            # Selects all data from the "usage_data" table
            cur.execute("SELECT DISTINCT homeid FROM homes")
            ids = [hid[0] for hid in cur.fetchall()]
            return ids
        except sqlite3.Error as e:
            print("GetAllHomeIDs: sqlite3 Error: ", e)
            return None
        except OSError as e:
            print("GetAllHomeIDs OSError: ", e)
            return None
        except Exception as e:
            print("GetAllHomeIDs error: ", e)
            return None
    else:
        return None
# END METHODS

# START CLASSES
# Home: Represents a home for organizing data based on home id
class Home():
    def __init__(self, homeid, database):
        self.datacols = ['homeid', 'deviceid', 'time', 'irms', 'pwr', 'pf', 'energy']
        self.tempcols = ['homeid', 'deviceid', 'time', 'temperature']
        self.id = homeid
        self.db = database
        self.data = None
        self.temp = None

    def __str__(self):
        return self.id

    # Changes the path to the database file
    def SetDatabaseFile(self, dbfile):
        self.db = dbfile

    # Usage data
    def GetData(self):
        return self.data

    def GetID(self):
        return self.id

    def GetPower(self):
        return self.data['pwr']

    def GetIRMS(self):
        return self.data['irms']

    def GetPowerFactor(self):
        return self.data['pf']

    def GetEnergy(self):
        return self.data['energy']

    def GetNumDataPts(self):
        return self.data.shape[0]

    # Temperature data
    def GetTemperature(self):
        return self.temp['temperature']

    def GetNumTempPts(self):
        return self.temp.shape[0]

    # Reads the data from selected database file that relates to this home server
    def ReadData(self, dbfile=None):
        # Can either pass in database file or use Home's database file
        if dbfile is None:
            dbfile = self.db
        # Make sure database exists
        if os.path.exists(dbfile):
            try:
                # Open connection with SQLite db
                con = sqlite3.connect(dbfile)
                cur = con.cursor()
                # "data" table data
                t = (self.id)
                cur.execute("SELECT * FROM data WHERE homeid = ?", t)
                self.data = cur.fetchall()
                self.data = pandas.DataFrame(self.data, columns=self.datacols)
                self.data['time'] = pandas.to_datetime(self.data['time'])
                # "temp" table data
                cur.execute("SELECT * FROM temp WHERE homeid = ?", t)
                self.temp = cur.fetchall()
                self.temp = pandas.DataFrame(self.temp, columns=self.tempcols)
                self.temp['time'] = pandas.to_datetime(self.temp['time'])
                # print(self.temp.info())
                con.close()
            except sqlite3.Error as e:
                print("Home ReadData: sqlite3 Error: ", e)
                return -1
            except OSError as e:
                print("Home ReadData OSError: ", e)
            except Exception as e:
                print("Home ReadData error: ", e)
        else:
            return -1


# It extends the Tkinter listbox to store representations of Home
# Manages the listbox and corresponding Home objects
class HomeList(tk.Listbox):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.data = dict()

    def insert(self, index, *elements):
        super().insert(index, *elements)
        for elem in elements:
            self.data[elem.GetID()] = elem

    def get(self, first, last=None):
        ids = super().get(first, last)
        if isinstance(ids, str):
            l = [self.data[i] for i in [ids]]
        else:
            l = [self.data[i] for i in ids]
        return tuple(l)

    def setDatabaseFile(self, dbfile):
        for k in self.data.keys():
            self.data[k].SetDatabaseFile(dbfile)

    # Returns true if home is already in list
    def isInList(self, id):
        if id in self.data.keys():
            return True
        return False

    def getByID(self, id):
        if self.isInList(id):
            return self.data[id]
        else:
            return None


# This tab should be added to a ttk.Notebook widget
# Pass in a ttk.Notebook as master
class HomeNotebookTab(tk.Frame):

    def __init__(self, home, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.output_csv = "D:\\Documents\\GitRepos\\central-server\\v2" \
                          "\\centralCode\\testout.csv"
        self.master = master
        self.home = home
        self.box = tk.Listbox(self, selectmode=tk.SINGLE)
        self.canvas = None
        self.buttonframe = tk.Frame(self)
        # Create buttons
        self.export = tk.Button(self.buttonframe, text="Export Home Data",
                           command=self.ExportHomeData)
        self.close = tk.Button(self.buttonframe, text="Close Tab",
                          command=self.CloseThisTab)
        self.filterframe = tk.Frame(self)
        self.filterbutton = tk.Button(self.filterframe, text="Filter",
                                      command=self.Filter)

        self.SetupTab()

        # Forget the currently selected tab
    def CloseThisTab(self, e=None):
        self.master.forget(self.master.select())

    def ExportHomeData(self, e=None):
        self.home.GetData().to_csv(self.output_csv)
        print(self.home.GetData())

    def Filter(self):
        try:
            data = self.home.GetData()
            start = datetime.datetime(int(self.ystart.get()),
                                      int(self.mstart.get()),
                                      int(self.dstart.get()))
            end = datetime.datetime(int(self.yend.get()),
                                      int(self.mend.get()),
                                      int(self.dend.get()))
            datamask = (data['time'] >= start) & (data['time'] <= end)
            print("start:", start, ", end:", end)
            datasubset = data.loc[datamask]
            datasubset = datasubset.sort_values(by=['time'])
            print(datasubset)
            self.chart = self.EmbedHomeDataChart(self, self.home, numpts=100, data=datasubset)
        except ValueError:
            pass


    # Takes in a dataframe with set of data and returns dataframe where
    # all points with equvalent datetime values are averaged
    def AverageDataOnSameTime(self, data):
        pass


    def SetupTab(self):
        # Create list of data related to specific home server
        self.box.pack(fill=tk.Y, side=tk.LEFT, expand=0)
        energy = self.home.GetEnergy()
        for i in energy[0:100]:
            self.box.insert(tk.END, str(i))

        # export.bind("<Button-1>", self.ExportHomeData)
        # close.bind("<Button-1>", self.CloseCurrentTab)
        self.export.pack(side=tk.LEFT)
        self.close.pack(side=tk.RIGHT)
        self.buttonframe.pack(side=tk.TOP)

        # Create date filters
        self.filterbutton.pack(side=tk.BOTTOM, fill=tk.X, expand=1)

        today = datetime.date.today()
        # Start date filters
        f = tk.Frame(self.filterframe)
        yel = tk.Label(f, text="End Year")
        self.yend = tk.Entry(f, bd=2)
        self.yend.insert(0, today.year)
        yel.pack(side=tk.TOP)
        self.yend.pack(side=tk.BOTTOM)
        f.pack(side=tk.RIGHT)

        f = tk.Frame(self.filterframe)
        mel = tk.Label(f, text="End Month")
        self.mend = tk.Entry(f, bd=2)
        self.mend.insert(0, today.month)
        mel.pack(side=tk.TOP)
        self.mend.pack(side=tk.BOTTOM)
        f.pack(side=tk.RIGHT)

        f = tk.Frame(self.filterframe)
        dela = tk.Label(f, text="End Day")
        self.dend = tk.Entry(f, bd=2)
        self.dend.insert(0, today.day)
        dela.pack(side=tk.TOP)
        self.dend.pack(side=tk.BOTTOM)
        f.pack(side=tk.RIGHT)

        l = tk.Label(self.filterframe, text="---->\n---->")
        l.pack(side=tk.RIGHT)

        f = tk.Frame(self.filterframe)
        ysl = tk.Label(f, text="Start Year")
        self.ystart = tk.Entry(f, bd=2)
        self.ystart.insert(0, today.year)
        ysl.pack(side=tk.TOP)
        self.ystart.pack(side=tk.BOTTOM)
        f.pack(side=tk.RIGHT)

        f = tk.Frame(self.filterframe)
        msl = tk.Label(f, text="Start Month")
        self.mstart = tk.Entry(f, bd=2)
        self.mstart.insert(0, today.month)
        msl.pack(side=tk.TOP)
        self.mstart.pack(side=tk.BOTTOM)
        f.pack(side=tk.RIGHT)

        f = tk.Frame(self.filterframe)
        dsl = tk.Label(f, text="Start Day")
        self.dstart = tk.Entry(f, bd=2)
        self.dstart.insert(0, today.day)
        dsl.pack(side=tk.TOP)
        self.dstart.pack(side=tk.BOTTOM)
        f.pack(side=tk.RIGHT)

        self.filterframe.pack(side=tk.BOTTOM)

        # Embed analytics chart in tab
        self.chart = self.EmbedHomeDataChart(self,
                                             self.home,
                                             numpts=min(self.home.GetNumDataPts(), 100))

    # Creates and embeds a figure displaying data for specific home server
    def EmbedHomeDataChart(self, master, home, numpts=5, data=None):
        if data is None:
            power = home.GetPower()
            irms = home.GetIRMS()
            energy = home.GetEnergy()
            powerfactor = home.GetPowerFactor()
            data_amount = home.GetNumDataPts()
        else:
            power = data['pwr']
            irms = data['irms']
            energy = data['energy']
            powerfactor = data['pf']
            data_amount = data.shape[0]


        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        if data_amount > 0:
            if data_amount <= numpts:
                numpts = data_amount
            fig = Figure(figsize=(5, 4), dpi=100)
            t = range(numpts)
            # Power
            ax = fig.add_subplot(221)
            ax.plot(t, power[data_amount - numpts:], 'r')
            # ax.axes.yaxis.set_ticks([])
            ax.axes.set_title("Power")
            # Power Factor
            ax = fig.add_subplot(222)
            ax.plot(t, powerfactor[data_amount - numpts:], 'y')
            # ax.axes.yaxis.set_ticks([])
            ax.axes.set_title("Power Factor")
            # Energy
            ax = fig.add_subplot(223)
            ax.plot(t, energy[data_amount - numpts:], 'b')
            # ax.axes.yaxis.set_ticks([])
            ax.axes.set_title("Energy")
            # IRMS
            ax = fig.add_subplot(224)
            ax.plot(t, irms[data_amount - numpts:], 'k')
            # ax.axes.yaxis.set_ticks([])
            ax.axes.set_title("IRMS")

            self.canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
# END CLASSES