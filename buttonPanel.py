import sys
import time
from tkinter import *
import tkinter.ttk as ttk

class ButtonPanel:
    def __init__(self, master=None, handler=None, buttonWidths=40, top=10, bottom=10):
        pass
    
    
if __name__ == '__main__':
    
    class TestButtonPanel(Frame):
        def __init__(self, master=None):
            Frame.__init__(self)              # Do superclass init
            self.pack()
            self.buttons = ButtonPanel(self)
            
        def do_somthing(self):
            pass
            
    root = Tk()
    root.title('The Button Panel')
    app = TestButtonPanel(master=root)
    app.mainloop()
    root.destroy()