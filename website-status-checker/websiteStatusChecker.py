#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Tue Feb  7 16:33:24 2017

@author: Jose Dzireh Chong
"""

#TODO:
    #Actually get this program working (debug to see what's wrong with it since I haven't worked on this in months)
    #Detect and clear previous output when button is pressed again
    #Make settings page

import requests
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

#credit to novel_yet_trivial for this class
class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=master.winfo_width()))

class InputArea(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
        self.ipPrompt = WrappingLabel(self, text="Enter website or IP address")
        self.ipInput = tk.Entry(self)
        self.ipInput.focus()
        self.submitButton = tk.Button(self, text="Check Status", command=self.master.outputArea.displayValidity)

        self.ipPrompt.pack()
        self.ipInput.pack()
        self.submitButton.pack()
        self.numericallyCorrect = None
        
    def attempt200ResponseCode(self):
        print("program still works as of beginning attempt200ResponseCode()") #for debugging purposes
        try:
            if len(self.ipInput.get().replace(" ", "")) == 0:
                return "Please input something"
            if "http://" not in self.ipInput.get().replace(" ", ""):
                websiteToCheck = "http://" + self.ipInput.get().replace(" ", "")
            else:
                websiteToCheck = "http://" + self.ipInput.get().replace(" ", "")
            r = requests.head(websiteToCheck)
            return r.status_code
        except requests.ConnectionError:
            return "Failed to connect"
        
    def setValidity(self):
        
        responseCode = self.attempt200ResponseCode()
        
        if str(responseCode)[0] in ["2", "3"]:
            self.numericallyCorrect = "Website is up and running"
            
        elif str(responseCode)[0] in ["4", "5"]:
            self.numericallyCorrect = "Website exists, but is either not running right now or doesn't have this subdomain"
        
        elif responseCode == "Failed to connect":
            self.numericallyCorrect = "Unknown whether website works or not, could not connect to it. Check your internet connection. It's possible this website doesn't even exist."
            
        elif responseCode == "Please input something":
            self.numericallyCorrect = "Please input something"
            
        else:
            self.numericallyCorrect = "Something's wrong. Contact me at josedzirehchong@gmail.com so I can attempt to resolve the issue."
            
        print(str(responseCode)) #for debugging purposes
        
class OutputArea(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.output = WrappingLabel(self, text="")
        self.output.pack()
        
    def displayValidity(self, event=None):
        self.master.inputArea.setValidity()
        outputVar = tk.StringVar()
        outputVar.set(self.master.inputArea.numericallyCorrect)
        self.master.inputArea.ipInput.delete(0,tk.END)
        self.output.config(textvariable=outputVar)
        
class MainWindow(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
        self.outputArea = OutputArea(self)
        self.inputArea = InputArea(self)
        
        self.inputArea.pack(fill=tk.X)
        self.outputArea.pack(fill=tk.X)
        
        self.master.bind('<Return>', self.outputArea.displayValidity)

def main():
    master = tk.Tk()
    master.title("Website Status Checker")
    master.geometry("400x400")
    win = MainWindow(master)
    win.pack(fill=tk.X)
    
    master.mainloop()

if __name__ == '__main__':
    main()
