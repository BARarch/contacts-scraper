import sys
import time
from tkinter import *
import tkinter.ttk as ttk
import queue
import threading




class ScraperControl:
    def __init__(self, master=None):
        self.frame = Frame(master)
        self.parent = master
        self.frame.pack()
        
        
        
        
if __name__ == '__main__':
    from scraperThread import *
    
    class TestScrapeControl(Frame):
        def __init__(self, master=None):
            Frame.__init__(self, master)              # Do superclass init
            self.parent = master
            self.pack()
            #self.control = ScraperControl(self)
            self.startupQueue = queue.Queue()
            self.commandQueue = queue.Queue()
            self.scraperQueue = queue.Queue()
            self.scraperProcess = ScraperThread(self.startupQueue, self.commandQueue, self.scraperQueue)
            self.numScrapes = 0
            self.scrapeSelection = StingVar(self)
            self.scrapeSelection.trace('w', self.change_dropdown)
            
        ## Handlers    
        
        def handle_scrape(self):
            
            # Initiates Scrape Thread Task
            self.commandQueue.put({'scrape': 'TODAY'})
            self.numScrapes = 0
            self.parent.after(100, self.manage_scrape)

        def handle_quit(self):
            
            # Ends Scraper Thread
            self.commandQueue.put({'stop': 1})
            self.quit()

        def startup(self):
            
            # Initiates Startup Thread Task
            self.scraperProcess.start()
            self.parent.after(100, self.manage_startup)



        ## Process Managers

        def manage_startup(self):
            # Processes Queue shared with startup tread task
            # Initialize Google Sheets for Write
            try:
                packet = self.startupQueue.get(0)
                #print(packet)
                if 'message' in packet:
                    msg = packet['message']
                    if msg == 'SCRAPE SESSION OPEN':
                        # Ready To Start
                        pass
                    else:
                        # Update Message and Keep Checking
                        
                        self.parent.after(100, self.manage_startup)

                if 'progress' in packet:
                    if packet['progress'] == 'FINNISHED':
                        pass
                    else:
                        
                        self.parent.after(100, self.manage_startup)

            except queue.Empty:
                self.parent.after(100, self.manage_startup)

        def manage_scrape(self):
            try:
                packet = self.scraperQueue.get(0)
                if 'done' in packet:
                    pass

                else:
                    if 'scraping' in packet:
                        self.numScrapes += 1
                        
                    if 'time' in packet:
                        pass
                    if 'numOrgs' in packet:
                        self.numOrgs = packet['numOrgs']

                    if 'report' in packet:
                        pass
                    
                    self.parent.after(100, self.manage_scrape)

            except queue.Empty:
                self.parent.after(100, self.manage_scrape)
    
    root = Tk()
    app = TestScrapeControl(master=root)
    app.after(500, app.startup)
    app.mainloop()
    root.destroy()
    
    
    
    
    
    



	





	
