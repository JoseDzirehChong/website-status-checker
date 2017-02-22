# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 16:33:24 2017

@author: Jose Chong
"""

import socket
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

class InputArea(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
        self.ipPrompt = tk.Label(self, text="Enter website or IP address")
        self.ipInput = tk.Entry(self)
        self.submitButton = tk.Button(self, text="Check Status", command=self.addValidOrNot)
        
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
            return address.count('.') == 3
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
        
    def checkStatus(self):
        websiteToCheck = self.ipInput.get().replace(" ", "")
        if self.is_valid_ipv4_address(websiteToCheck) or self.is_valid_ipv6_address(websiteToCheck):
            return "Valid"
            if len(websiteToCheck) == 0:
                return "Please input something"
        return "Invalid"
        
    def addValidOrNot(self):
        self.checkStatus()
        validOrNot = tk.Label(self.master.outputArea, text=self.checkStatus())
        validOrNot.pack()
        self.ipInput.delete(0,tk.END)
    
class OutputArea(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

class MainWindow(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
        self.inputArea = InputArea(self)
        self.outputArea = OutputArea(self)
        
        self.inputArea.pack()
        self.outputArea.pack()

def main():
    master = tk.Tk()
    master.title("IP Status Checker")
    master.geometry("300x300")
    win = MainWindow(master)
    win.pack(fill=tk.X)
    master.mainloop()

if __name__ == '__main__':
    main()
