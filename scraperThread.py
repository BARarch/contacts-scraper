import pandas as pd
import scraperModelGS as smgs

import directoryManager as dm
import contactChecker as cc

import sys
import time

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



class ScraperThread(threading.Thread):
    def __init__(self, startupHandle, commandHandle, scraperHandle):
        threading.Thread.__init__(self)
        self.startupQueue = startupHandle
        self.commandQueue = commandHandle
        self.scraperQueue = scraperHandle
        
    def run(self):         
        self.start_scraper()
       
        ## Scraper Loop
        self.commandLoop = True
        
        while self.commandLoop:
            self.commandLoop = self.listen_for_cmd()
        
        cc.VerificationHandler.close_browser()
        print('SCRAPER THREAD FINNISHED')
        
    def start_scraper(self):
        get_credentials_method = smgs.modelInit()

        # Get Headers from google sheets
        print('KEYS')
        self.startupQueue.put({'progress': 'START'})
        self.startupQueue.put({'message': 'KEYS'})
        contactKeys = getContactKeys(get_credentials_method)
        self.startupQueue.put({'progress': 1})
        directoryKeys = getAgencyDirKeys(get_credentials_method)
        self.startupQueue.put({'progress': 2})
        print('')

        # Get contact and orginization website data and structure with collected headings
        print('RECORDS')
        self.startupQueue.put({'message': 'RECORDS'})
        contactRecords = [sheetRecord(row, contactKeys) for row in getContacts(get_credentials_method)]
        self.startupQueue.put({'progress': 3})
        self.orgRecords = [sheetRecord(row, directoryKeys) for row in getAgencyDir(get_credentials_method)]
        self.startupQueue.put({'progress': 4})
        print('')

        # Create Dataframes
        cr = pd.DataFrame(contactRecords)
        dr = pd.DataFrame(self.orgRecords)
        print('DATAFRAMES READY') 
        self.startupQueue.put({'message': 'DATAFRAMES READY',
                        'progress': 5})
        ## //////////////////  Initialize Contact Checker Classes with Fresh Data  \\\\\\\\\\\\\\\\\\\

        # Setup Contact Record Output
        cc.ContactSheetOutput.set_output(contactKeys)
        self.startupQueue.put({'progress': 6})
        # For this scrape session Give the Verification Handler class an Orgsession with Organization Records
        dm.OrgSession.set_browser_path()                                 ## IMPORTANT STEP: The browser path must be set to the current working directory which varies for different machines
        cc.VerificationHandler.set_orgRecords(dm.HeadlessOrgSession(self.orgRecords))
        self.startupQueue.put({'progress': 7})
        # For this scrape session Give the Verification Handler class the contact record data
        cc.VerificationHandler.set_contactRecords(cr)
        
        cc.ScrapeSession.set_app_scraper_queue(self.scraperQueue)
        cc.ScrapeSession.set_app_command_queue(self.commandQueue)
        print('CONTACT CHECKER READY')
        

        print('SCRAPE SESSION OPEN')
        print('')
        self.startupQueue.put({'message': 'SCRAPE SESSION OPEN',
                               'progress': 'FINNISHED'})

            
    def listen_for_cmd(self):
        while True:
            try:
                packet = self.commandQueue.get(0)
                ## Scrape Events
                if 'scrape' in packet:
                    if packet['scrape'] == 'TODAY':
                        print('The scraper is running')
                        t = cc.ScrapeForToday(self.orgRecords)
                        
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