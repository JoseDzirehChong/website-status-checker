#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Tue Feb  7 16:33:24 2017

@author: Jose Dzireh Chong
"""

import socket
import requests
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

class InputArea(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
        self.ipPrompt = tk.Label(self, text="Enter website or IP address")
        self.ipInput = tk.Entry(self)
        self.submitButton = tk.Button(self, text="Check Status", command=self.master.outputArea.displayValidity)

        self.ipPrompt.pack()
        self.ipInput.pack()
        self.submitButton.pack()
        
    #credit to http://stackoverflow.com/a/4017219 for the two functions below

    def is_valid_ipv4_address(self, address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_pton()
            except socket.error:
                return False
            return True
        except socket.error:  # not a valid address
            return False

        return True

    def is_valid_ipv6_address(self, address):
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_pton()
            except socket.error:
                return False
        except socket.error:  # not a valid address
            return False

        return True

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
        try:
            responseCode = int(responseCode)
        except ValueError:
            pass
        if str(responseCode)[0] in ["2", "3"]:
            self.numericallyCorrect = tk.Label(self.master.outputArea, text="Website is up and running")
        if str(responseCode)[0] in ["4", "5"]:
            self.numericallyCorrect = tk.Label(self.master.outputArea, text="Website exists, but is either not running right now or doesn't have this subdomain")
        elif responseCode == "Failed to connect":
            self.numericallyCorrect = tk.Label(self.master.outputArea, text="Unknown whether website works or not, could not connect to it. Check your internet connection. It's possible this website doesn't even exist.")
        elif responseCode == "Please input something":
            self.numericallyCorrect = tk.Label(self.master.outputArea, text=responseCode)
        else:
            self.numericallyCorrect = tk.Label(self.master.outputArea, text="something's wrong")
        print(responseCode) #for debugging purposes
class OutputArea(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
    def displayValidity(self):
        self.master.inputArea.setValidity()
        self.master.inputArea.numericallyCorrect.pack()
        self.master.inputArea.ipInput.delete(0,tk.END)

class MainWindow(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
        self.outputArea = OutputArea(self)
        self.inputArea = InputArea(self)
        
        self.inputArea.pack()
        self.outputArea.pack()

def main():
    master = tk.Tk()
    master.title("Website Status Checker")
    master.geometry("400x400")
    win = MainWindow(master)
    win.pack(fill=tk.X)
    master.mainloop()

if __name__ == '__main__':
    main()
