import sys
import time
from tkinter import *
import tkinter.ttk as ttk

class StatusBar:
    def __init__(self, master=None):
        self.frame = Frame(master)
        self.parent = master
        self.frame.pack(side=BOTTOM, fill=X, anchor=W)
        
        self.mainStatus = Label(self.frame, bd=1, anchor=W, relief=SUNKEN, text="Hello")
        self.mainStatus.pack(side=LEFT, anchor=W, expand=True, fill=X)
        
        self.timeStatus = Label(self.frame, bd=1, relief=SUNKEN, width=12, text="There")
        self.timeStatus.pack(side=RIGHT, anchor=E)
        
    def message(self, msg):
        self.mainStatus.configure(text=msg)
        self.frame.update()
        
    def clear_message(self):
        self.mainStatus.configure(text="")
        self.frame.update()
        
    def stamp(self, stamp):
        self.timeStatus.configure(text=stamp)
        self.frame.update()
        
    def clear_stamp(self):
        self.timeStatus.configure(text="")
        self.frame.update()