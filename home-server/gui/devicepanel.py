import tkinter as tk
from tkinter import ttk

import mariadb
import subprocess
import pandas as pd

class Device():#Todo: open a connection to mariadb via pandas and import the data here

    def __init__(self, device_info, recorded_data):
        self.setDeviceInfo(device_info) 
        self.data = recorded_data
        #self.id set in setDeviceInfo
        #self.name set in setDeviceInfo >> setName
        #self.isPlug set in setDeviceInfo

    def setDeviceInfo(self, metadata):
        self.id = metadata["id"]
        self.setName(metadata["name"]) 
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

class DevicePanel(tk.Frame):

    def __init__(self, master=None, device=None):
        super().__init__(master)
        self.device = device
        self.createWidgets()

    def togglePower(self): # need to do feedback and error checking on this one
        subprocess.run(["../communications/connectsd.sh", self.device.id])
        if self.device.getState == 1: # currently running, turn off
            subprocess.run(["../communications/relayc.sh"])
        elif self.device.getState == 0: # currently off, turn on
            subprocess.run(["../communications/relayb.sh"])
        subprocess.run(["../communications/disconnect.sh"])
        return

    def createWidgets(self):
        self.toggleButton = tk.Button(self, text="Toggle Power", command=self.togglePower)
        #self.dataTbl = TABLE(self, data)
        #self.graph = GRAPH(self, data)

