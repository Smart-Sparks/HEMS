import tkinter as tk
from tkinter import ttk

import mariadb
import subprocess
import pandas as pd
import pandastable as pt
import functions as f

import pathlib
import os
from os.path import join

class Device():

    def __init__(self, info=None, data=None):
        self.setDeviceInfo(info) 
        self.data = data
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
        curr.execute(f'UPDATE devices SET name = "{new_name}" WHERE id={self.getID()}')
        conn.commit()
        conn.close()
        print(f"changed name for device {self.getID()} from {self.name} to {new_name}")
        self.name = new_name
        return

    def getData(self):
        return self.data

    def exportCSV(self):
        #FIXME
        self.data.to_csv(f"~/{self.getType()} {self.name}.csv", index=False)
        #print("Error occurred trying to export a device to CSV.")
        return

class DeviceTable(pt.Table):
    
    def __init__(self, master=None, data=None):
        super().__init__(master, dataframe=data)
         

class DeviceInfoFrame(tk.Frame):
    
    def __init__(self, master=None, device=None):
        super().__init__(master)
        self.device = device
        self.createWidgets()
        self.configureGUI()
        return

    def getInput(self):
        return self.nameBox.get("1.0", tk.END)

    def changeName(self):
        text = self.getInput().rstrip() # remove trailing whitespace
        if(text):
            if text.isalnum():
                self.device.changeName(text) 
            else:
                print("changeName: alphanumeric only!")
        else:
            pass
        return

    def createWidgets(self):
        self.changeNameLabel = tk.Label(self, text="New Name:")
        self.toggleButton = tk.Button(self, text="Toggle Power", command=self.master.togglePower, relief=tk.RAISED)
        self.changeNameButton = tk.Button(self, text="Change Device Name", command=self.changeName, relief=tk.RAISED)
        self.nameBox = tk.Text(self, height=1) #TODO: name changing text box 
        self.exportCSVButton = tk.Button(self, text="Export to CSV", command=self.device.exportCSV)
        return

    def configureGUI(self):
        self.changeNameLabel.grid(row=0, column=0, sticky="E")
        self.toggleButton.grid(row=0, column=3, sticky="E")
        self.changeNameButton.grid(row=0, column=2, sticky="E")
        self.nameBox.grid(row=0, column=1, sticky="E")
        self.exportCSVButton.grid(row=0, column=4, sticky="E")
        return




class DevicePanel(tk.Frame):

    def __init__(self, master=None, device=None):
        super().__init__(master)
        self.device = device
        self.createWidgets()
        self.configureGUI()

    def togglePower(self): # need to do feedback and error checking on this one
        #try:
        pathtocomms = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "communications") 
        if self.device.getState(): # currently running, turn off
            print("Turning off.")
            print(["bash", os.path.join(pathtocomms, "relayc.sh")])
            subprocess.run(["bash", os.path.join(pathtocomms, "relayc.sh")])
        else: # currently off, turn on
            print("Turning on.")
            print(["bash", os.path.join(pathtocomms, "relayb.sh")])
            subprocess.run(["bash", os.path.join(pathtocomms, "relayb.sh")])
        #subprocess.run(["bash", os.path.join(pathtocomms, "disconnect.sh")])
        self.device.toggleState() # update in representations
        #except:
        #    print("Error trying to toggle power for the device.")
        #self.device.toggleState() # test it out here
        return

    # setDevice: put a new device in
    def setDevice(self, device):
        self.device = device
        # might have to call something to redraw dataTbl and graph
        return

    def createWidgets(self):
        self.headerPanel = DeviceInfoFrame(self, self.device) #FIXME
        self.TblFrame = tk.Frame(self)
        self.dataTbl = DeviceTable(self.TblFrame, self.device.getData()) #self.dataTbl = TABLE(self, data)
        #self.graph = GRAPH(self, data)
        return
    
    def configureGUI(self):
        #self.toggleButton.grid(row=0, column=0, columnspan=5)
        #self.dataTbl.grid(row=6, column=0, columnspan=5)
        #self.dataTbl.show()
        #self.toggleButton.pack(side=tk.RIGHT)
        self.headerPanel.pack(side=tk.TOP)
        self.TblFrame.pack(side=tk.BOTTOM)
        self.dataTbl.show()
        self.master.title(f"ID {self.device.getID()}: {self.device.getName()} {self.device.getType()}")
        return



class DeviceWindow(tk.Toplevel):
    
    def __init__(self, master=None, device=None): 
        super().__init__(master)
        self.createWidgets(selected_device=device)
    
    def createWidgets(self, selected_device):
        self.panel = DevicePanel(self, selected_device)
        self.panel.pack(expand=True, fill=tk.BOTH)  
