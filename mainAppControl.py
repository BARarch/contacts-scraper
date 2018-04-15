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
from spreadSheetControl import *




class MainApplication(Frame):
    def __init__(self, master=None):
        Frame.__init__(self)
        self.parent = master
        self.pack()
        
        self.startupQueue = queue.Queue()
        self.commandQueue = queue.Queue()
        self.scraperQueue = queue.Queue()
        self.rowCounts = {'contact counts': 0,
                          'scraper counts': 0}
        
        self.scrapeMode = None
        self.scrapeSelection = StringVar(self)
        self.scrapeSelection.trace('w', self.change_dropdown)
        
        self.indicators = InitPanel(self)
        ttk.Separator(self).pack(side=TOP, fill=X, padx=2)
        self.control = ScraperControl(self, self)
        ttk.Separator(self).pack(side=TOP, fill=X, padx=2)
        self.manager = SpreadSheetControl(self, self)
        self.statusBar = StatusBar(self)
        self.scraperProcess = ScraperThread(self.startupQueue, self.commandQueue, self.scraperQueue)
        ttk.Separator(self).pack(side=TOP, fill=X, padx=2)

        
        self.numScrapes = 0
        self.report = None
        

    ## Handlers    

    def handle_scrape(self):
        # Initiates Scrape Thread Task
        self.commandQueue.put({'scrape': self.scrapeMode})
        self.indicators._contactChecker.on(why='IN USE')
        self.control.buttons.disable_dropdown()
        self.control.buttons.disable_scrape()
        self.manager.disable_restore()
        self.manager.disable_transfer()
        self.manager.update_transfer_status()
        self.numScrapes = 0
        self.report = None
        self.statusBar.message("Scraper is running...")
        self.parent.after(100, self.manage_scrape)

    def handle_quit(self):
        # Ends Scraper Thread
        self.commandQueue.put({'stop': 1})
        self.quit()
        
    def change_dropdown(self, *args):
        self.scrapeMode = self.scrapeSelection.get()
        self.commandQueue.put({'sheet change': self.scrapeMode})

    def handle_restore(self):
        self.commandQueue.put({'restore': 1})
        self.control.progress.message("Restoring Contacts...")
        self.statusBar.message("Restoring")
        self.control.buttons.disable_scrape()
        self.manager.disable_restore()
        self.manager.disable_transfer()
        self.parent.after(100, self.manage_restore())

    def handle_transfer(self):
        self.commandQueue.put({'transfer': 1})
        self.control.progress.message("Transfering Contacts...")
        self.statusBar.message("Transfering")
        self.control.buttons.disable_scrape()
        self.manager.disable_restore()
        self.manager.disable_transfer()
        self.parent.after(100, self.manage_transfer()) 

    def startup(self):
        # Initiates Startup Thread Task
        self.scraperProcess.start()
        self.statusBar.message("Startup")
        self.statusBar.stamp('--')
        self.control.progress.message("Loading...")
        self.control.parse.lightOff()
        self.scrapeMode = self.scrapeSelection.get()
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
                    self.manager.enable_restore()
                    self.manager.update_transfer_status(self.rowCounts)
                else:
                    self.statusBar.message(msg)
            if '__waiting' in packet:
                whosWaiting = packet['__waiting']
                if whosWaiting is ScraperThread.ContactKeysVal:
                    self.indicators.contact_keys_waiting()
                if whosWaiting is ScraperThread.DirectoryKeysVal:
                    self.indicators.directory_keys_waiting()
                if whosWaiting is ScraperThread.ContactRecordsVal:
                    self.indicators.contact_records_waiting()
                if whosWaiting is ScraperThread.AgencyDirectoryVal:
                    self.indicators.agency_directory_waiting()
                if whosWaiting is ScraperThread.DataVal:
                    self.indicators.data_waiting()
                if whosWaiting is ScraperThread.OutputVal:
                    self.indicators.output_waiting()
                if whosWaiting is ScraperThread.BrowserDriverVal:
                    self.indicators.browser_driver_waiting()
                if whosWaiting is ScraperThread.ContactCheckerVal:
                    self.indicators.scraper_waiting()     
            if '__ready' in packet:
                whosReady = packet['__ready']
                if whosReady is ScraperThread.ContactKeysVal:
                    self.indicators.contact_keys_ready()
                if whosReady is ScraperThread.DirectoryKeysVal:
                    self.indicators.directory_keys_ready()
                if whosReady is ScraperThread.ContactRecordsVal:
                    self.indicators.contact_records_ready()
                if whosReady is ScraperThread.AgencyDirectoryVal:
                    self.indicators.agency_directory_ready()
                if whosReady is ScraperThread.DataVal:
                    self.indicators.data_ready()
                if whosReady is ScraperThread.OutputVal:
                    self.indicators.output_ready()
                if whosReady is ScraperThread.BrowserDriverVal:
                    self.indicators.browser_driver_ready()
                if whosReady is ScraperThread.ContactCheckerVal:
                    self.indicators.scraper_open_phase()
            if 'rowCounts' in packet:
                self.rowCounts = packet['rowCounts']  
            if 'progress' in packet:
                if packet['progress'] == 'START':
                    self.control.progress.set_progress_clicks(8) 
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
            comeBack = True
            packet = self.scraperQueue.get(False)
            print('__scrape:', packet)
            if 'done' in packet:
                self.statusBar.message("Ready")
                if self.report:
                    self.control.progress.message("Scrape Completed In {}".format(self.report['time of scrape']))
                else:
                    self.control.progress.message("Scrape Completed In --:--:--")
                self.control.buttons.enable_dropdown()
                self.control.buttons.enable_scrape()
                self.manager.enable_restore()
                self.manager.update_transfer_status(self.rowCounts)
                self.indicators._contactChecker.off()
                comeBack = False    
            if 'scraping' in packet:
                self.numScrapes += 1
                self.control.progress.message("Scraping: {}".format(packet['scraping']))
            if 'complete' in packet:
                self.control.progress.advance()
                self.statusBar.stamp('')         
            if 'time' in packet:
                self.statusBar.stamp(packet['time'])
            if 'numOrgs' in packet:
                self.numOrgs = packet['numOrgs']
                self.control.progress.set_progress_clicks(self.numOrgs)
            if 'rowCounts' in packet:
                self.rowCounts = packet['rowCounts']
            if 'report' in packet:
                self.report = packet['report']
            if '__DIRON' in packet:
                if packet['__DIRON'] == "__recordRow":
                    self.indicators.agency_report_on()
            if '__DIROFF' in packet:
                self.indicators.agency_report_off()
            if '__OUTON' in packet:
                self.indicators.output_on()
            if '__OUTOFF' in packet:
                self.indicators.output_off()
            if '__PARSEON' in packet:
                self.control.parse.lightOn()
            if '__PARSEOFF' in packet:
                self.control.parse.lightOff()
            if '__REQUESTON' in packet:     
                self.indicators.request_on()
            if '__REQUESTOFF' in packet:
                self.indicators.request_off()

            if comeBack:
                self.parent.after(100, self.manage_scrape)

        except queue.Empty:
            self.parent.after(100, self.manage_scrape)

    def manage_transfer(self):
        try:
            comeBack = True
            packet = self.scraperQueue.get(False)
            print('__transfer:', packet)
            if 'done' in packet:
                self.control.progress.message("Contacts Transfered")
                self.control.buttons.enable_scrape()
                self.manager.enable_restore()
                self.manager.update_transfer_status(self.rowCounts)
                self.statusBar.message("Ready")
                comeBack = False
            if 'rowCounts' in packet:
                self.rowCounts = packet['rowCounts']
            if '__OUTON' in packet:
                self.indicators.output_on()
            if '__OUTOFF' in packet:
                self.indicators.output_off()

            if comeBack:
                self.parent.after(100, self.manage_transfer)

        except queue.Empty:
            self.parent.after(100, self.manage_transfer)

    def manage_restore(self):
        try:
            comeBack = True
            packet = self.scraperQueue.get(False)
            print('__restore:', packet)
            if 'done' in packet:
                self.control.progress.message("Contacts Restored")
                self.control.buttons.enable_scrape()
                self.manager.enable_restore()
                self.manager.update_transfer_status(self.rowCounts)
                self.statusBar.message("Ready")
                comeBack = False
            if 'rowCounts' in packet:
                self.rowCounts = packet['rowCounts']    
            if '__OUTON' in packet:
                self.indicators.output_on()
            if '__OUTOFF' in packet:
                self.indicators.output_off()

            if comeBack:
                self.parent.after(100, self.manage_restore)

        except queue.Empty:
            self.parent.after(100, self.manage_restore)

class MainApplicationGD(MainApplication):
    def __init__(self, master=None):
        Frame.__init__(self)
        self.parent = master
         
        self.startupQueue = queue.Queue()
        self.commandQueue = queue.Queue()
        self.scraperQueue = queue.Queue()
        self.rowCounts = {'contact counts': 0,
                          'scraper counts': 0}
        
        self.scrapeMode = None
        self.scrapeSelection = StringVar(self)
        self.scrapeSelection.trace('w', self.change_dropdown)
        
        self.indicators = InitPanelGD(self)
        ttk.Separator(self).grid(sticky=E+W, pady=5)
        self.control = ScraperControlGD(self, self)
        ttk.Separator(self).grid(sticky=E+W, pady=5)
        self.manager = SpreadSheetControlGD(self, self)
        ttk.Separator(self).grid(sticky=E+W)
        self.statusBar = StatusBarGD(self)
        self.scraperProcess = ScraperThread(self.startupQueue, self.commandQueue, self.scraperQueue)
        
        self.numScrapes = 0
        self.report = None

        self.grid()
        
        
        
        
if __name__ == '__main__':
        
    
    root = Tk()
    app = MainApplicationGD(master=root)
    #app.after(500, app.startup)
    app.mainloop()
    root.destroy()
    
    
    
    
    
    



	





	
