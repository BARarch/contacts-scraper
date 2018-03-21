import sys
import time
from tkinter import *
import tkinter.ttk as ttk
from testLeds import *

PanelColor = '#545454'

class LEDRow(Frame):
    def __init__(self, master=None, name="NONE"):
        Frame.__init__(self, master)
        self.parent = master
        self.pack(expand=True, side=LEFT)
        self.config(width=300, height=300, background='red')
        self.update()
        
        self.indicator = LED(master=self.parent, appearance=FLAT, shape=ROUND, blink=1, blinkrate=1, bd=1).frame.pack(  side=LEFT,
                                                        expand=YES, 
                                                        padx=5, 
                                                        pady=1)
        self.name = Label(self, text=name).pack(expand=True, fill=BOTH, side=LEFT)
        self.status = Label(self, relief=SUNKEN,fg="red", text='Waiting', width=20).pack(expand=True, fill=BOTH, side=RIGHT)


root = Tk()
root.title('LED Row')
app = LEDRow(master=root, name='Contact Keys')
app.mainloop()
root.destroy()