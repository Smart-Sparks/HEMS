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
## END IMPORTS

##########
#FUNCTIONS
##########

#connectMDB returns the connection
#maybe should move this to a class that closes the connection upon the destruction occurring?
def connectMDB():
    try: 
        conn = mariadb.connect(user='root', password='', host='localhost', database='hems')
        conn.autocommit = False
        print("Successfully connected to the database.")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn

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
             


class MainPanel(tk.Frame):

    def __init__(self, master=None):        
        super().__init__(master)
        self.configureGUI()
        self.createWidgets()

    def pullDeviceData(self):
        ##pulls the device data from the database and populates the deviceList with these objects
        ##open connection with mariadb
        conn = connectMDB() 
        devices_table = pd.read_sql_query("SELECT * FROM devices;", conn)
        for index, row in devices_table.iterrows():  
            if row["plug"]:
                recorded_data = pd.read_sql_query("SELECT * FROM energy;", conn)
            else:
                recorded_data = pd.read_sql_query("SELECT * FROM temperature;", conn)
            new_device = dp.Device(row, recorded_data)
            self.deviceList.insert(tk.END, new_device)
        conn.close()
        ##TODO: FINISH PULLDEVICEDATA/  

    def createWidgets(self):
        self.window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.window.pack(fill=tk.BOTH, expand=True)
        self.deviceList = DeviceList(master=self, selectmode="SINGLE") 
        self.pullDeviceData() ##populate the deviceList
        #self.deviceList.pack(side=tk.LEFT, expand=True, fill='y')
        self.dataPanel = dp.DevicePanel(self)
        #self.dataPanel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.window.add(self.deviceList)
        self.window.add(self.dataPanel)
        return

    def configureGUI(self):
        self.master.title("HEMS")
        return


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x600")
        app = MainPanel(master=self)
        app.pack()

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
