import sys
import time
from tkinter import *
import tkinter.ttk as ttk
import queue
import threading

from scraperThread import *
from initPanel import *
from scraperControl import *
from statusBar import *




class MainApplication(Frame):
    def __init__(self, master=None):
        Frame.__init__(self)
        self.parent = master
        self.pack()
        
        self.startupQueue = queue.Queue()
        self.commandQueue = queue.Queue()
        self.scraperQueue = queue.Queue()
        
        self.scrapeMode = None
        self.scrapeSelection = StringVar(self)
        self.scrapeSelection.trace('w', self.change_dropdown)
        
        self.indicators = InitPanel(self)
        ttk.Separator(self).pack(side=TOP, fill=X, padx=2)
        self.control = ScraperControl(self, self)
        self.statusBar = StatusBar(self)
        self.scraperProcess = ScraperThread(self.startupQueue, self.commandQueue, self.scraperQueue)
        
        self.numScrapes = 0
        

    ## Handlers    

    def handle_scrape(self):

        # Initiates Scrape Thread Task
        self.commandQueue.put({'scrape': 'TODAY'})
        self.control.buttons.disable_scrape()
        self.numScrapes = 0
        self.parent.after(100, self.manage_scrape)

    def handle_quit(self):
        # Ends Scraper Thread
        self.commandQueue.put({'stop': 1})
        self.quit()
        
    def change_dropdown(self, *args):
        self.scrapeMode = self.scrapeSelection.get() 

    def startup(self):

        # Initiates Startup Thread Task
        self.scraperProcess.start()
        self.parent.after(100, self.manage_startup())



    ## Process Managers

    def manage_startup(self):
        # Processes Queue shared with startup tread task
        # Initialize Google Sheets for Write
        try:
            packet = self.startupQueue.get(0)
            print(packet)
            if 'message' in packet:
                msg = packet['message']
                if msg == 'SCRAPE SESSION OPEN':
                    self.control.buttons.enable_scrape()
                else:
                    # Update Message and Keep Checking

                    self.parent.after(100, self.manage_startup)

            if 'progress' in packet:
                if packet['progress'] == 'START':
                    self.control.progress.set_progress_clicks(7)
                    self.parent.after(100, self.manage_startup()) 
                elif packet['progress'] == 'FINNISHED':
                    self.control.progress.advance()
                    
                else:
                    self.control.progress.advance()
                    
                    self.parent.after(100, self.manage_startup())
                    

        except queue.Empty:
            self.parent.after(100, self.manage_startup)

    def manage_scrape(self):
        try:
            packet = self.scraperQueue.get(0)
            print(packet)
            if 'done' in packet:
                self.control.buttons.enable_scrape()

            else:
                if 'scraping' in packet:
                    self.numScrapes += 1
                    
                if 'complete' in packet:
                    self.control.progress.advance()
                    
                if 'time' in packet:
                    pass
                if 'numOrgs' in packet:
                    self.numOrgs = packet['numOrgs']
                    self.control.progress.set_progress_clicks(self.numOrgs)
                if 'report' in packet:
                    pass
                

                self.parent.after(100, self.manage_scrape)

        except queue.Empty:
            self.parent.after(100, self.manage_scrape)
        
        
        
        
if __name__ == '__main__':
        
    
    root = Tk()
    app = MainApplication(master=root)
    app.after(500, app.startup)
    app.mainloop()
    root.destroy()
    
    
    
    
    
    



	





	
