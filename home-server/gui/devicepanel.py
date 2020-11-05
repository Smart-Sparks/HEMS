import tkinter as tk
from tkinter import ttk

import mariadb
import subprocess
import pandas as pd

class Device():#Todo: open a connection to mariadb via pandas and import the data here
    def __init__(self, device_info, recorded_data):
        self.setDeviceInfo(device_info) 
        self.data = recorded_data
    def setDeviceInfo(self, metadata):
        self.id = device_info["id"][0]
        self.
class DevicePanel(tk.Frame):
    def __init__(self, device):
        super().__init__(master)
        self.device = device
        self.toggleButton = tk.Button(self, text="Toggle Power", command=self.togglePower)
        #self.dataTbl = TABLE(self, data)
        #self.graph = GRAPH(self, data)
    def togglePower(self): # need to do feedback and error checking on this one
        subprocess.run(["../communications/connectsd.sh", self.device.id])
        if self.device.getState == 1: # currently running, turn off
            subprocess.run(["../communications/relayc.sh"])
        elif self.device.getState == 0: # currently off, turn on
            subprocess.run(["../communications/relayb.sh"])
        subprocess.run(["../communications/disconnect.sh"])
