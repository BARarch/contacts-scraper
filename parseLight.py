import sys
import time
from tkinter import *
import tkinter.ttk as ttk
from testLeds import *

class ParseLightPanel:
    def __init__(self, master=None, width=7, top=2, bottom=10):
        # Has a frame
        self.frame = Frame(master)
        self.parent = master
        self.frame.pack()
        Label(self.frame, text="Parse").pack(side=TOP, expand=True, fill=X, pady=1)
        self.indicator = LED(master=self.frame, appearance=FLAT, shape=ROUND, blink=0, blinkrate=1, bd=0, outline='grey')
        self.indicator.frame.pack(side=TOP, expand=YES, padx=5, pady=5)
        
    def lightOn(self):
        self.indicator.alarm()
        return self
        
    def lightOff(self):
        self.indicator.turnoff()
        return self

class ParseLightPanelGD(ParseLightPanel):
    def __init__(self, master=None, width=7, top=2, bottom=10):
        pass
    
if __name__ == '__main__':
    
    class TestParseLightPanel(Frame):
        def __init__(self, master=None):
            Frame.__init__(self)              # Do superclass init
            self.parent = master
            self.pack()
            self.blinkState = False
            self.parseLight = ParseLightPanel(self).lightOff()
            
        def blink(self):
            if self.blinkState:
                self.blinkState = False
                self.parseLight.lightOff()
            else:
                self.blinkState = True
                self.parseLight.lightOn()     
            self.after(500, self.blink)
            
    root = Tk()
    root.title('The Parse Light')
    app = TestParseLightPanel(master=root)
    app.after(500, app.blink)
    app.mainloop()
    root.destroy()