from tkinter import *
import tkinter.ttk as ttk
from ledRow import *

class InitPanel:
    def __init__(self, master=None):
        self.frame = Frame(master)
        self.parent = master
        self.frame.pack(expand=True, side=TOP, anchor=N)
        self.left = Frame(self.frame)
        self.left.pack(side=LEFT, anchor=N, expand=True)
        self.right = Frame(self.frame)
        self.right.pack(side=RIGHT, anchor=N, expand=True)
        
        self._contactKeys = LEDRow(self.left, name="Contact Keys").off()
        self._directoryKeys = LEDRow(self.left, name="Directory Keys").off()   
        self._contactRecords = LEDRow(self.left, name="Contact Records").off()
        self._agencyDirectory = LEDRow(self.left, name="Agency Directory").off()
        
        self._data = LEDRow(self.right, name="Data").off().waiting()
        self._output = LEDRow(self.right, name="Output").off().waiting()
        self._browserDriver = LEDRowNoMsg(self.right, name="Browser/Driver").off()
        self._contactChecker = LEDRow(self.right, name="Contact Checker").off()
        
    ## Startup Phases
    
    
    # Contact Scraper Open
    
    # Contact Scraper Running
        

if __name__ == '__main__':
    
    class TestInitPanel(Frame):
         def __init__(self, master=None):
            Frame.__init__(self, master)              # Do superclass init
            self.pack()
            InitPanel(self)
            
    root = Tk()
    root.title('LED Row')
    app = TestInitPanel(master=root)
    app.mainloop()
    root.destroy()