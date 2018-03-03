import pandas as pd
import scraperModelGS as smgs

import directoryManager as dm
import contactChecker as cc

import sys
import time
from tkinter import *
import tkinter.ttk as ttk
import queue
import threading

def getContacts(get_credentials_method):
    """Google Sheets API Code.
    Pulls urls for all NFL Team RSS Feeds
    https://docs.google.com/spreadsheets/d/1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs/
    """
    credentials = get_credentials_method()
    http = credentials.authorize(smgs.httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = smgs.discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    #specify sheetID and range
    spreadsheetId = '1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs'
    rangeName = 'Contacts!A2:N'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found for Contact Records.')
    else:
        print('Contact Records Done')

    return values

def getContactKeys(get_credentials_method):
    """Google Sheets API Code.
    Pulls urls for all NFL Team RSS Feeds
    https://docs.google.com/spreadsheets/d/1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs/
    """
    credentials = get_credentials_method()
    http = credentials.authorize(smgs.httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = smgs.discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    #specify sheetID and range
    spreadsheetId = '1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs'
    rangeName = 'Contacts!A1:Q1'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName, majorDimension="ROWS").execute()
    values = result.get('values', [])

    if not values:
        print('No data found Contact Keys.')
    else:
        print('Contact Keys Done')

    return values[0]

def getAgencyDir(get_credentials_method):
    """Google Sheets API Code.
    Pulls urls for all NFL Team RSS Feeds
    https://docs.google.com/spreadsheets/d/1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs/
    """
    credentials = get_credentials_method()
    http = credentials.authorize(smgs.httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = smgs.discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    #specify sheetID and range
    spreadsheetId = '1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs'
    rangeName = 'Org Leadership Websites!A2:E'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found for Agency Directory.')
    else:
        print('Agency Directory Done')

    return values

def getAgencyDirKeys(get_credentials_method):
    """Google Sheets API Code.
    Pulls urls for all NFL Team RSS Feeds
    https://docs.google.com/spreadsheets/d/1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs/
    """
    credentials = get_credentials_method()
    http = credentials.authorize(smgs.httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = smgs.discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    #specify sheetID and range
    spreadsheetId = '1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs'
    rangeName = 'Org Leadership Websites!A1:Q1'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found for Directory Keys.')
    else:
        print('Directory Keys Done')

    return values[0]

def sheetRecord(row, recordKeys):
    '''
        record['Account ID'] = row[0]
        record['Account Name'] = row[1]
        record['Contact ID'] = row[2]
        record['First Name'] = row[3]
        record['Last Name'] = row[4]
        record['Tittle'] = row[5]
        record['Email'] = row[6]
        record['Mailing Street'] = row[7]
        record['Mailing City'] = row[8]
        record['Mailing State'] = row[9]
        record['Mailing Zip'] = row[10]
        record['Mailing Country'] = row[11]
        record['Phone'] = row[12]
        record['Contact Source'] = row[13]
    
        recordKeys = ['Account ID', 'Account Name', ...]
    
    '''
    key = 0
    record = {}
    
    ## Copy all elements from sheet row read
    for elm in row:
        record[recordKeys[key]] = elm
        key += 1
    
    ## Fill in remainder with empty strings
    while key < len(recordKeys):
        record[recordKeys[key]] = ''
        key += 1
    
    return record








class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.parent = master
        self.pack()
        
        self.fmStartupStatus = Frame().pack(expand=True, fill=BOTH, side=TOP)
        self.fmStatus = Frame().pack(expand=True, fill=BOTH, side=TOP)
        self.create_startup_status(self.fmStartupStatus)
        self.create_status(self.fmStatus)
        
        self.fmControl = Frame().pack(side=BOTTOM)
        self.create_widgets(self.fmControl)
        
        ## Application Process Flags
        self.startupFlag = False
        
        
    def create_widgets(self, panel):
        self.progressBarPosition = 0
        self.QUIT = Button(panel)
        self.QUIT.configure(command=self.handle_quit,
                            text='QUIT',
                            fg='red')        
        self.QUIT.pack(side=LEFT)
        
        self.SCRAPE = Button(panel)
        self.SCRAPE.configure(command=self.handle_scrape,
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
        
    def move_progress(self, pos):
        points = (pos * self.pb['maximum'])
        delta = int(points - self.pb['value'])
        
        for i in range(delta):
            self.pb.step()
            self.update()
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
            self.update()
            time.sleep(.02)
        
        #print('Value ' + str(self.pb['value']))
        
    def complete_startup_progress(self):
        self.startupFlag = True
        self.pb.step()
        self.update
        
        #print('Value ' + str(self.pb['value']))

    def handle_scrape(self):
        self.SCRAPE.config(state='disabled')
        self.commandQueue.put({'scrape': 'TODAY'})
        self.parent.after(100, self.manage_scrape)
        
    def handle_quit(self):
        self.commandQueue.put({'stop': 1})
        self.quit()
        
    def startup(self):
        # Initiates Startup Tread Task
        self.startupQueue = queue.Queue()
        self.commandQueue = queue.Queue()
        self.scraperQueue = queue.Queue()
        self.change_status("LOADING")
        self.scraperProcess = ScraperThread(self.startupQueue, self.commandQueue, self.scraperQueue)
        self.scraperProcess.start()
        self.parent.after(100, self.manage_startup)
        
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
                    self.change_startup_status(msg)
                    self.change_status('')
                    self.SCRAPE.configure(state='active', fg='green')
                else:
                    # Update Message and Keep Checking
                    self.change_startup_status(msg)
                    self.parent.after(100, self.manage_startup)
                    
            if 'progress' in packet:
                if packet['progress'] == 'FINNISHED':
                    self.complete_startup_progress()
                else:
                    pro = packet['progress']
                    self.move_progress_start(pro / 7)
                    self.parent.after(100, self.manage_startup)
                
        except queue.Empty:
            self.parent.after(100, self.manage_startup)
    
    def manage_scrape(self):
        try:
            packet = self.scraperQueue.get(0)
            if 'done' in packet:
                self.SCRAPE.config(state='active')
                
            else:
                if 'scraping' in packet:
                    pass
                if 'time' in packet:
                    pass
                if 'numOrgs' in packet:
                    pass
                if 'report' in packet:
                    pass
                self.parent.after(100, self.manage_scrape)
            
        except queue.Empty:
            self.parent.after(100, self.manage_scrape)
            
 




            
class ScraperThread(threading.Thread):
    def __init__(self, startupHandle, commandHandle, scraperHandle):
        threading.Thread.__init__(self)
        self.startupQueue = startupHandle
        self.commandQueue = commandHandle
        self.scraperQueue = scraperHandle
        
    def run(self):         
        get_credentials_method = smgs.modelInit()

        # Get Headers from google sheets
        print('KEYS')
        self.startupQueue.put({'progress': 1})
        self.startupQueue.put({'message': 'KEYS'})
        contactKeys = getContactKeys(get_credentials_method)
        self.startupQueue.put({'progress': 2})
        directoryKeys = getAgencyDirKeys(get_credentials_method)
        self.startupQueue.put({'progress': 3})
        print('')

        # Get contact and orginization website data and structure with collected headings
        print('RECORDS')
        self.startupQueue.put({'message': 'RECORDS'})
        contactRecords = [sheetRecord(row, contactKeys) for row in getContacts(get_credentials_method)]
        self.startupQueue.put({'progress': 4})
        orgRecords = [sheetRecord(row, directoryKeys) for row in getAgencyDir(get_credentials_method)]
        self.startupQueue.put({'progress': 5})
        print('')

        # Create Dataframes
        cr = pd.DataFrame(contactRecords)
        dr = pd.DataFrame(orgRecords)
        print('DATAFRAMES READY') 
        self.startupQueue.put({'message': 'DATAFRAMES READY',
                        'progress': 6})
        ## //////////////////  Initialize Contact Checker Classes with Fresh Data  \\\\\\\\\\\\\\\\\\\

        # Setup Contact Record Output
        cc.ContactSheetOutput.set_output(contactKeys)
        self.startupQueue.put({'progress': 7})
        # For this scrape session Give the Verification Handler class an Orgsession with Organization Records
        dm.OrgSession.set_browser_path()                                 ## IMPORTANT STEP: The browser path must be set to the current working directory which varies for different machines
        cc.VerificationHandler.set_orgRecords(dm.HeadlessOrgSession(orgRecords))
        #self.queue.put({'progress': 'Finishd'})
        # For this scrape session Give the Verification Handler class the contact record data
        cc.VerificationHandler.set_contactRecords(cr)
        print('CONTACT CHECKER READY')
        
        
        ## //////////////////        Scrape Base Case and Turn Off Browser         \\\\\\\\\\\\\\\\\\\

        print('SCRAPE SESSION OPEN')
        print('')
        self.startupQueue.put({'message': 'SCRAPE SESSION OPEN',
                               'progress': 'FINNISHED'})

        self.commandLoop = True
        
        while self.commandLoop:
            self.commandLoop = self.listen_for_cmd()
            
        print('SCRAPER THREAD FINNISHED')

            
    def listen_for_cmd(self):
        while True:
            try:
                packet = self.commandQueue.get(0)
                ## Scrape Events
                if 'scrape' in packet:
                    if packet['scrape'] == 'TODAY':
                        print('The scraper is running')
                        time.sleep(5)
                        print('scraper finnished')
                        print('')
                        self.scraperQueue.put({'done':1})
                    return True
                
                ## Stop Events
                if 'stop' in packet:
                    print('scraper loop done')
                    return False
                
            except queue.Empty:
                time.sleep(.2)
        

        
        
        
        
        
        
        
        
if __name__ == '__main__':
    
    root = Tk()
    app = Application(master=root)
    app.after(500, app.startup)
    app.mainloop()
    root.destroy()
    
   
    
    



	





	
