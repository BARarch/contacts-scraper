import sys
import time
from tkinter import *
import tkinter.ttk as ttk
import testLeds as LED

class Row(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.parent = master
        self.pack()
        
        self.led = Label(self, text='LED').pack(expand=True, fill=BOTH, side=LEFT)
        self.fmScraperControlPanel = Label(self, text='ContactRecords').pack(expand=True, fill=BOTH, side=LEFT)
        self.status = Label(self, relief=SUNKEN, text='Waiting').pack(expand=True, fill=BOTH, side=RIGHT)


root = Tk()
root.title('Contacts Pane')
app = Row(master=root)
app.mainloop()
root.destroy()