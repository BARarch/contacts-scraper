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
        self.indicators._contactChecker.on(why='IN USE')
        self.control.buttons.disable_scrape()
        self.control.buttons.disable_dropdown()
        self.numScrapes = 0
        self.statusBar.message("Scraper is running...")
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
        self.statusBar.message("Startup")
        self.statusBar.stamp('--')
        self.control.progress.message("Loading...")
        self.control.parse.lightOff()
        self.parent.after(100, self.manage_startup())



    ## Process Managers

    def manage_startup(self):
        # Processes Queue shared with startup tread task
        # Initialize Google Sheets for Write
        comeBack = True
        try:
            packet = self.startupQueue.get(False)
            print('__startup:', packet)
            if 'message' in packet:
                msg = packet['message']
                if msg == 'SCRAPE SESSION OPEN':
                    self.control.buttons.enable_scrape()
                    self.control.buttons.enable_dropdown()
                    self.control.progress.message("Scrape Session Open")
                    self.statusBar.message("Ready")
                else:
                    self.statusBar.message(msg)
                    

            if '__waiting' in packet:
                whosWaiting = packet['__waiting']
                if whosWaiting is ScraperThread.ContactKeysVal:
                    pass
                if whosWaiting is ScraperThread.DirectoryKeysVal:
                    pass
                if whosWaiting is ScraperThread.ContactRecordsVal:
                    pass
                if whosWaiting is ScraperThread.AgencyDirectoryVal:
                    pass
                if whosWaiting is ScraperThread.DataVal:
                    pass
                if whosWaiting is ScraperThread.OutputVal:
                    pass
                if whosWaiting is ScraperThread.BrowserDriverVal:
                    pass
                if whosWaiting is ScraperThread.ContactCheckerVal:
                    pass
                
            if '__ready' in packet:
                whosReady = packet['__ready']
                if whosReady is ScraperThread.ContactKeysVal:
                    pass
                if whosReady is ScraperThread.DirectoryKeysVal:
                    pass
                if whosReady is ScraperThread.ContactRecordsVal:
                    pass
                if whosReady is ScraperThread.AgencyDirectoryVal:
                    pass
                if whosReady is ScraperThread.DataVal:
                    pass
                if whosReady is ScraperThread.OutputVal:
                    pass
                if whosReady is ScraperThread.BrowserDriverVal:
                    pass
                if whosReady is ScraperThread.ContactCheckerVal:
                    pass
                
            if 'progress' in packet:
                if packet['progress'] == 'START':
                    self.control.progress.set_progress_clicks(8)
                    self.parent.after(100, self.manage_startup()) 
                elif packet['progress'] == 'FINNISHED':
                    self.control.progress.advance()
                    self.indicators._contactChecker.off()
                    comeBack = False                    ## Terminate Startup Loop
                else:
                    self.control.progress.advance()
            
            if comeBack:
                self.parent.after(100, self.manage_startup())
                             

        except queue.Empty:
            self.parent.after(100, self.manage_startup)

    def manage_scrape(self):
        try:
            packet = self.scraperQueue.get(False)
            print('__scrape:', packet)
            if 'done' in packet:
                self.statusBar.message("Ready")
                self.control.progress.message("Scrape Completed In --:--:--")
                self.control.buttons.enable_scrape()
                self.control.buttons.enable_dropdown()
                self.indicators._contactChecker.off()
                
            else:
                if 'scraping' in packet:
                    self.numScrapes += 1
                    self.control.progress.message("Scraping: {}".format(packet['scraping']))
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
    
    
    
    
    
    



	





	
