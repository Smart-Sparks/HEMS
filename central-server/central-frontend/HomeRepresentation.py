# HomeRepresentation.py

# START IMPORTS
import tkinter as tk

from tkinter import ttk

import numpy as np

import sqlite3
import os
import pandas
import csv
# END IMPORTS

# START CLASSES
# Home: Represents a home for organizing data based on home id
class Home():
    def __init__(self, homeid, database):
        self.id = homeid
        self.db = database
        self.data = []

    def __str__(self):
        return self.id

    # Changes the path to the database file
    def SetDatabaseFile(self, dbfile):
        self.db = dbfile

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
                # Selects all data from the "usage_data" table
                cur.execute('''SELECT * from usage_data''')
                self.data = cur.fetchall()
                # for row in cur.fetchmany(10):
                #     print(row)
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

        # numDataPts = 300
        # t = np.arange(0, 3, .01)
        # self.data = 2 * np.sin(2 * np.pi * t) + np.random.rand(numDataPts)*0.1

    def GetData(self):
        return self.data

    def GetID(self):
        return self.id

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
# END CLASSES