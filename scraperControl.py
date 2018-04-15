import sys
import time
from tkinter import *
import tkinter.ttk as ttk
import queue
import threading

from buttonPanel import *
from progressPanel import *
from parseLight import *


ControlSidePadding = 13

class ScraperControl:
    def __init__(self, master=None, handler=None):
        self.frame = Frame(master)
        self.parent = master
        self.frame.pack(side=TOP, padx=5)
        
        self.left = Frame(self.frame)
        self.left.pack(side=LEFT, expand=True, anchor=N, pady=7) 
        self.buttonHandler = handler
        #self.scrapeSelection = StringVar(self)
        #self.scrapeSelection.trace('w', self.buttonHandler.change_dropdown)  # Event handler function for dropdown in handler object
        self.buttons = ButtonPanel(self.left, self.buttonHandler)
        
        self.center = Frame(self.frame)
        self.center.pack(side=LEFT, anchor=N, expand=True, pady=10, padx=5)
        self.progress = ProgressPanel(self.center)
        
        self.right = Frame(self.frame)
        self.right.pack(side=LEFT, expand=True, padx=10, pady=10, anchor=N)
        self.parse = ParseLightPanel(self.right)
        
        #self.frame.update()
        
class ScraperControlGD(ScraperControl):
    def __init__(self, master=None, handler=None):
        self.frame = Frame(master)
        self.parent = master
         
        #self.left.pack(side=LEFT, expand=True, anchor=N, pady=7) 
        self.buttonHandler = handler
        self.buttons = ButtonPanelGD(self.frame, self.buttonHandler)
        
        #self.center.pack(side=LEFT, anchor=N, expand=True, pady=10, padx=5)
        self.progress = ProgressPanelGD(self.frame)
        
        #self.right.pack(side=LEFT, expand=True, padx=10, pady=10, anchor=N)
        self.parse = ParseLightPanelGD(self.frame) 

        self.frame.grid(sticky=E+W, padx=ControlSidePadding)
        self.frame.columnconfigure(2, pad=21)
        self.frame.columnconfigure(3, pad=41)
        Frame(self.frame).grid(row=2, pady=5)

        #self.frame.pack(side=TOP, padx=5)  
        
        
        
        
if __name__ == '__main__':
    from scraperThread import *
    
    class TestScrapeControl(Frame):
        def __init__(self, master=None):
            Frame.__init__(self)
            self.pack()
            self.scrapeSelection = StringVar(self)
            self.scrapeSelection.trace('w', self.change_dropdown)   # Event handler function for dropdown in handler frame
            self.control = ScraperControlGD(self, self)
            
            self.scrapeMode = 'Today'
            self.control.parse.lightOff()
            self.control.buttons.enable_scrape()
            self.control.buttons.disable_quit()
            self.control.progress.set_progress_clicks(4)            # Progress Bar is reset
        
            
        ## Handlers    
        def handle_scrape(self):
            self.control.buttons.enable_quit()
            self.control.buttons.disable_dropdown()
            self.control.buttons.disable_scrape()
            self.control.parse.lightOn()
            self.control.progress.advance()
            
            
        def handle_quit(self):
            self.control.buttons.disable_quit()
            self.control.buttons.enable_dropdown()
            self.control.buttons.enable_scrape()
            if self.control.progress.done():
                self.control.progress.message('Scrape is Done')
            self.control.parse.lightOff()
            
        def change_dropdown(self, *args):
            self.scrapeMode = self.scrapeSelection.get()
            self.control.progress.message(self.scrapeMode)
            self.control.progress.set_progress_clicks(4)            # Progress Bar is reset
        
            
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
    
    
    
    
    
    



	





	
