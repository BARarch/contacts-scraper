import sys
import time
from tkinter import *
import tkinter.ttk as ttk


class ProgressPanel:
    def __init__(self, master=None width=50, top=10, bottom=10):
        pass
    
    
if __name__ == '__main__':
    
    class TestProgressPanel(Frame):
        def __init__(self, master=None):
            Frame.__init__(self)              # Do superclass init
            self.pack()
            
            self.ProgressPanel = ProgressPanel(self)
            
        def move(self):
            pass
            
    root = Tk()
    root.title('The Progress Panel')
    app = TestProgressPanel(master=root)
    app.mainloop()
    root.destroy()