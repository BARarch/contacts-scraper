import sys
import time
from tkinter import *
import tkinter.ttk as ttk
from testLeds import *

#PanelColor = '#545454'
LABELWIDTH = 20
STATUSWIDTH = 10

class LEDRow:
    def __init__(self, master=None, name="NONE", blink=0, blinkrate=1):
        self.frame = Frame(master, width=300, height=300) 
        self.parent = master
        self.frame.pack(expand=True, side=TOP, anchor=W, fill=X)
        
        self.indicator = LED(master=self.frame, appearance=FLAT, shape=ROUND, blink=blink, blinkrate=blinkrate, bd=0, outline='grey').frame.pack(side=LEFT, anchor=W, expand=YES, padx=5, pady=1)
        self.name = Label(self.frame, text=name, anchor=W, width=LABELWIDTH).pack(side=LEFT,  fill=BOTH, pady=5)
        self.status = Label(self.frame, relief=SUNKEN,fg="red", text='Waiting', width=STATUSWIDTH).pack(expand=True, fill=Y, side=RIGHT,anchor=E)
        
if __name__ == '__main__':
    
    class TestLEDRow(Frame):
         def __init__(self, master=None):
            Frame.__init__(self)              # Do superclass init
            self.pack()
            LEDRow(self, name="The Test Row", blink=1)
            LEDRow(self, name="The Second Row", blink=1, blinkrate=2)
            LEDRow(self, name="The Third Row")
            
    root = Tk()
    root.title('LED Row')
    app = TestLEDRow(master=root)
    app.mainloop()
    root.destroy()