import tkinter as tk
from tkinter import ttk

import mariadb
import subprocess
import pandas as pd

import functions as f

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

class Device():

    def __init__(self, device_info, recorded_data):
        self.setDeviceInfo(device_info) 
        self.data = recorded_data
        #self.id set in setDeviceInfo
        #self.name set in setDeviceInfo >> setName
        #self.isPlug set in setDeviceInfo

    def setDeviceInfo(self, metadata):
        self.id = metadata["id"]
        self.setName(metadata["name"]) 
        self.state = metadata["status"]
        if(metadata["plug"]):
            self.isPlug = True
        else:
            self.isPlug = False
        return

    def setName(self, name=None):
        if name:
            self.name = name
        else:
            self.name = "Unnamed"
        return

    def getName(self):
        return self.name

    #def setDeviceName(self, new_name):
        #upon certain events, change the device name

    def getID(self):
        return self.id

    def getType(self):
        devicetype=""
        if(self.isPlug):
            devicetype="Smart Plug"
        else:
            devicetype="Smart Thermometer"
        return devicetype

    def getState(self):
        return self.state

    def toggleState(self):
        self.state = not self.state
        # update in database
        conn = f.connectMDB()
        curr = conn.cursor() 
        curr.execute(f"UPDATE devices SET status = NOT status WHERE id={self.getID()}") 
        conn.commit()
        conn.close()
        print(f"toggling state for device {self.getID()}")
        return

    def changeName(self, new_name):
        # update in database
        conn = f.connectMDB()
        curr = conn.cursor()
        curr.execute(f"UPDATE devices SET name = new_name WHERE id={self.getID()}")
        conn.commit()
        conn.close()
        print(f"changed name for device {self.getID()} from {self.name} to {new_name}")
        self.name = new_name
        return

class DevicePanel(tk.Frame):

    def __init__(self, master=None, device=None):
        super().__init__(master)
        self.device = device
        self.createWidgets()
        self.configureGUI()

    def togglePower(self): # need to do feedback and error checking on this one
        try:
            if self.device.getState(): # currently running, turn off
                subprocess.run(["../communications/relayc.sh"])
            elif self.device.getState(): # currently off, turn on
                subprocess.run(["../communications/relayb.sh"])
            subprocess.run(["../communications/disconnect.sh"])
        except:
            print("Error trying to toggle power for the device.")
        self.device.toggleState() # FIXME: move into try block
        return

    # setDevice: put a new device in
    def setDevice(self, device):
        self.device = device
        # might have to call something to redraw dataTbl and graph
        return

    def createWidgets(self):
        self.toggleButton = tk.Button(self, text="Toggle Power", command=self.togglePower)
        #self.dataTbl = TABLE(self, data)
        #self.graph = GRAPH(self, data)
        return
    
    def configureGUI(self):
        self.toggleButton.grid(row=0, column=0, columnspan=5)
        return
