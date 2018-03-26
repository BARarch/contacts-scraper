import sys
import time
from tkinter import *
import tkinter.ttk as ttk
import queue
import threading

from buttonPanel import *
from progressPanel import *
from parseLight import *




class ScraperControl:
    def __init__(self, master=None, handler=None):
        self.frame = Frame(master)
        self.parent = master
        self.frame.pack()
        
        self.left = Frame(self.frame)
        self.left.pack(side=LEFT, expand=True) 
        self.buttonHandler = handler
        #self.scrapeSelection = StringVar(self)
        #self.scrapeSelection.trace('w', self.buttonHandler.change_dropdown)  # Event handler function for dropdown in handler object
        self.buttons = ButtonPanel(self.left, self.buttonHandler)
        
        self.center = Frame(self.frame)
        self.center.pack(side=LEFT, expand=True)
        self.progress = ProgressPanel(self.center)
        
        self.right = Frame(self.frame)
        self.right.pack(side=LEFT, expand=True)
        self.parse = ParseLightPanel(self.right)
        
        #self.frame.update()
        
        
        
        
        
        
if __name__ == '__main__':
    from scraperThread import *
    
    class TestScrapeControl(Frame):
        def __init__(self, master=None):
            Frame.__init__(self)
            self.pack()
            self.scrapeSelection = StringVar(self)
            self.scrapeSelection.trace('w', self.change_dropdown)  # Event handler function for dropdown in handler frame
            self.control = ScraperControl(self, self)
            #self.update()
        
            
        ## Handlers    
        def handle_scrape(self):
            pass
            
        def handle_quit(self):
            pass
            
        def change_dropdown(self, *args):
            pass
            
        def startup(self):
            pass
            



        ## Process Managers

        def manage_startup(self):
            #see mainAppControl
            pass

        def manage_scrape(self):
            #see mainAppControl
            pass
    
    root = Tk()
    app = TestScrapeControl(master=root)
    app.after(500, app.startup)
    app.mainloop()
    root.destroy()
    
    
    
    
    
    



	





	
