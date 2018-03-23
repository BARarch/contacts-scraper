import sys
import time
from tkinter import *
import tkinter.ttk as ttk
from testLeds import *

class ParseLightPanel:
    def __init__(self, master=None width=20, top=10, bottom=10):
        pass
    
    
if __name__ == '__main__':
    
    class TestParseLightPanel(Frame):
        def __init__(self, master=None):
            Frame.__init__(self)              # Do superclass init
            self.pack()
            self.blinkState = False
            self.parseLight = ParseLightPanel(self)
            
        def blink(self):
            pass
            
    root = Tk()
    root.title('The Parse Light')
    app = TestParseLightPanel(master=root)
    app.mainloop()
    root.destroy()