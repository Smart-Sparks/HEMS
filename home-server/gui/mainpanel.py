# mainpanel.py
# William Plucknett
# The main panel of the home server gui.
# Ideas taken from Chase Vickery's implementation of the Central Server GUI

# IMPORTS
import tkinter as tk
from tkinter import ttk

import mariadb
import sys
import devicepanel as dp
import pandas as pd
import functions as f
## END IMPORTS


########
#CLASSES
########

#DeviceList expands the tk.Listbox object to handle features of the devices
class DeviceList(tk.Listbox):

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.data = []

    def insert(self, index, *elements):
        #super().insert(index, *elements)
        for elem in elements:
            self.data.append(elem)
            super().insert(index, f"{elem.getID()}: {elem.getName()} {elem.getType()}")
    
    # return the device at the index in data
    def getDevice(self, idx):
        return self.data[idx]


class MainPanel(tk.Frame):

    def __init__(self, master=None):        
        super().__init__(master)
        self.createWidgets()
        self.configureGUI()

    def pullDeviceData(self):
        ##pulls the device data from the database and populates the deviceList with these objects
        ##open connection with mariadb
        conn = f.connectMDB() 
        devices_table = pd.read_sql_query("SELECT * FROM devices;", conn)
        for index, row in devices_table.iterrows():  
            print(f"HERE:{row['plug']}")
            if row["plug"]:
                recorded_data = pd.read_sql_query("SELECT * FROM energy;", conn)
            else:
                recorded_data = pd.read_sql_query("SELECT * FROM temperature;", conn)
            new_device = dp.Device(info=row, data=recorded_data)
            self.deviceList.insert(tk.END, new_device)
        conn.close()
        return

    ## viewSelected: open a new window to show data relevant to the selected device
    def viewSelected(self):
        selection = self.deviceList.curselection()
        if(selection):
            displayMe = self.deviceList.getDevice(selection[0])
            newWindow = dp.DeviceWindow(self, device=displayMe)
            devpanel = dp.DevicePanel(master=newWindow, device=displayMe)
            devpanel.pack(expand=True, fill=tk.BOTH)
        return

    ## refresh: refreshes the list view, in case name change or device added
    def refresh(self):
        self.deviceList.delete(0, tk.END)
        self.pullDeviceData()
        return

    def createWidgets(self):
        self.deviceList = DeviceList(master=self, selectmode="SINGLE", relief=tk.SUNKEN) 
        self.buttonpanel = tk.Frame(self)
        self.pullDeviceData() ##populate the deviceList
        #self.dataPanel = dp.DevicePanel(self)
        self.viewButton = tk.Button(self.buttonpanel, text="View", command=self.viewSelected, relief=tk.RAISED)
        self.refreshButton = tk.Button(self.buttonpanel, text="Refresh", command=self.refresh, relief=tk.RAISED)
        return

    def configureGUI(self):
        self.master.title("HEMS")
        #self.deviceList.grid(row=0, column=0, rowspan=2, sticky="NW")
        #self.dataPanel.grid(row=0, column=1, rowspan=3, columnspan=2, sticky="NE")
        #self.viewButton.grid(row=3, column=0, sticky="SW")
        self.deviceList.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.buttonpanel.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        self.viewButton.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.refreshButton.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        return

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("200x600")
        app = MainPanel(master=self)
        app.pack(expand=True, fill=tk.BOTH)
        return

    def Run(self):
        self.mainloop()

############
#END CLASSES
############

def main():
    app = App()
    app.Run()

if __name__ == "__main__":
    main()
