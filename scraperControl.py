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
        
        self.fmStartupStatus = Frame(self.frame).pack(expand=True, fill=BOTH, side=TOP)
        self.fmStatus = Frame(self.frame).pack(expand=True, fill=BOTH, side=TOP)
        self.create_startup_status(self.fmStartupStatus)
        self.create_status(self.fmStatus)
        
        self.fmControl = Frame(self.frame).pack(side=BOTTOM)
        self.create_widgets(self.fmControl)
        
        ## Application Process Flags
        self.startupFlag = False
        self.scrapeFlag = False
        
        
        
    def create_widgets(self, panel):
        self.progressBarPosition = 0
        self.QUIT = Button(panel)
        self.QUIT.configure(command=self.parent.handle_quit,
                            text='QUIT',
                            fg='red')
        self.QUIT.pack(side=LEFT)
        
        self.SCRAPE = Button(panel)
        self.SCRAPE.configure(command=self.parent.handle_scrape,
                              text='Scrape',
                              fg='green',
                              state='disabled')
        self.SCRAPE.pack(side=LEFT)
        
        self.pb = ttk.Progressbar(panel)
        self.pb.configure(orient='horizontal',
                          length=400,
                          mode='determinate',
                          maximum=200,
                          variable=self.progressBarPosition)
        self.pb.pack(side=LEFT)

    ## Status Bars 
        
    def create_startup_status(self, panel):
        self.startupStatus = Label(panel, text='STARTUP STATUS')
        self.startupStatus.pack()
        
    def change_startup_status(self, msg):
        self.startupStatus.configure(text=msg)
        
    def create_status(self, panel):
        self.status = Label(panel, text='MAIN STATUS')
        self.status.pack()
        
    def change_status(self, msg):
        self.status.configure(text=msg)
              
        
    ## Progress Bar Opperations
        
    def move_progress(self, pos):
        points = (pos * self.pb['maximum'])
        delta = int(points - self.pb['value'])
        
        for i in range(delta):
            self.pb.step()
            self.frame.update()
            time.sleep(.02)
        #print(self.progressBarPosition)
        #print('Value ' + str(self.pb['value']))
        #print('Var ' + str(self.pb['variable']))
        
    def move_progress_start(self, pos):
        points = pos * self.pb['maximum'] - 1
        
        while self.pb['value'] < points:
            if self.startupFlag:
                print('Halted Status Bar')
                return
            self.pb.step()
            self.frame.update()
            time.sleep(.02)
            
    def move_progress_scrape(self, pos):
        points = pos * self.pb['maximum'] - 1
        
        while self.pb['value'] < points:
            if self.scrapeFlag:
                print('Halted Status Bar')
                return
            self.pb.step()
            self.frame.update()
            time.sleep(.02)
        
        #print('Value ' + str(self.pb['value']))
        
    def complete_startup_progress(self):
        self.startupFlag = True
        self.pb.step()
        self.frame.update()
        
    def complete_scrape_progress(self):
        self.scrapeFlag = True
        self.pb.step()
        self.frame.update()
        
        #print('Value ' + str(self.pb['value']))

    def lower_scrape_flag(self):
        self.scrapeFlag = False
        
        
if __name__ == '__main__':
    from scraperThread import *
    
    class TestScrapeControl(Frame):
        def __init__(self, master=None):
            Frame.__init__(self, master)              # Do superclass init
            self.parent = master
            self.pack()
            self.control = ScraperControl(self)
            self.startupQueue = queue.Queue()
            self.commandQueue = queue.Queue()
            self.scraperQueue = queue.Queue()
            self.scraperProcess = ScraperThread(self.startupQueue, self.commandQueue, self.scraperQueue)
            self.numScrapes = 0
            
        ## Handlers    
        
        def handle_scrape(self):
            self.control.SCRAPE.config(state='disabled')
            self.control.change_startup_status('SCRAPER IS RUNNING...')
            self.commandQueue.put({'scrape': 'TODAY'})
            self.numScrapes = 0
            self.control.lower_scrape_flag()
            self.parent.after(100, self.manage_scrape)

        def handle_quit(self):
            self.commandQueue.put({'stop': 1})
            self.quit()

        def startup(self):
            # Initiates Startup Tread Task
            self.control.change_status("LOADING")
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
                        self.control.change_startup_status(msg)
                        self.control.change_status('')
                        self.control.SCRAPE.configure(state='active', fg='green')
                    else:
                        # Update Message and Keep Checking
                        self.control.change_startup_status(msg)
                        self.parent.after(100, self.manage_startup)

                if 'progress' in packet:
                    if packet['progress'] == 'FINNISHED':
                        self.control.complete_startup_progress()
                    else:
                        pro = packet['progress']
                        self.control.move_progress_start(pro / 7)
                        self.parent.after(100, self.manage_startup)

            except queue.Empty:
                self.parent.after(100, self.manage_startup)

        def manage_scrape(self):
            try:
                packet = self.scraperQueue.get(0)
                if 'done' in packet:
                    self.control.change_startup_status('SCRAPE SESSION OPEN')
                    self.control.change_status('Scrape Completed in --:--:--')
                    self.control.complete_scrape_progress()
                    self.control.SCRAPE.config(state='active')

                else:
                    if 'scraping' in packet:
                        self.numScrapes += 1
                        self.control.change_status('Scraping ' + packet['scraping'] )
                        self.control.move_progress_scrape(self.numScrapes / self.numOrgs)
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
    
    
    
    
    
    



	





	
