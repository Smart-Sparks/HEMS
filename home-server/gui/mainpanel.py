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
        self.data = data
    def insert(self, index, *elements):
        super().insert(index, *elements)
        for elem in elements:
            self.data[elem.getID()] = elem
             
class MainPanel(tk.Frame):
    def __init__(self, master=None):        
        super().__init__(master)
        self.master.title("HEMS")
        self.deviceList = DeviceList(master=self, selectmode="SINGLE") 
        self.deviceList.insert()
        self.deviceList.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    def pullDeviceData(self):
        ##pulls the device data from the database and populates the deviceList with these objects
        ##open connection with mariadb
        conn = connectMDB() 
        device_info = pd.read_sql_query("SELECT * FROM devices;", conn)
        if device_info["plug"]:
            recorded_data = pd.read_sql_query("SELECT * FROM energy;", conn)
        else:
            recorded_data = pd.read_sql_query("SELECT * FROM temperature;", conn)
            new_device = dp.Device(device_info, recorded_data)
            
        conn.close()
        ##TODO: FINISH PULLDEVICEDATA/  
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
