#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Tue Feb  7 16:33:24 2017

@author: Jose Dzireh Chong
"""

#TODO:
    #Make settings page

import requests
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

#credit to /u/dreamer_jake for changing the way I got the response code and used it to display the output
#credit to /u/novel_yet_trivial for this class
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
        
    def check_status(self, url):
        
        url = "".join(url.split())
        if url == "":
            return "Please input something"
        if "http://" not in url:
            url = "http://" + url
        try:
            if str(requests.get(url).status_code)[0] in self.master.code_descriptions:
                return self.master.code_descriptions.get(str(requests.get(url).status_code)[0], "Unknown")
        except requests.ConnectionError:
            return "Failed to connect (unknown whether website works or not - website may possibly be non-existent), please check your url"
        
    def setValidity(self):
        
        print(self.check_status(self.ipInput.get())) #for debugging purposes
        return self.check_status(self.ipInput.get())
        
class OutputArea(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.output = WrappingLabel(self, text="")
        self.output.pack()
        
    def displayValidity(self, event=None):
        output = self.master.inputArea.setValidity()
        outputVar = tk.StringVar()
        outputVar.set(output)
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
        
        self.code_descriptions = {
                '2': "Website is up and running",
                '3': "Website is up and running",
                '4': "Website exists, but is either not running right now, doesn't have this subdomain, or you don't have the permission to access it",
                '5': "Website exists, but is either not running right now, doesn't have this subdomain, or you don't have the permission to access it"
                }

def main():
    master = tk.Tk()
    master.title("Website Status Checker")
    master.geometry("400x400")
    win = MainWindow(master)
    win.pack(fill=tk.X)
    
    master.mainloop()

if __name__ == '__main__':
    main()
