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
    
    ContactKeysVal = 'ck'
    DirectoryKeysVal = 'dk'
    ContactRecordsVal = 'cr'
    AgencyDirectoryVal = 'ad'
    DataVal = 'd'
    OutputVal = 'o'
    BrowserDriverVal = 'bd'
    ContactCheckerVal = 'cc'
    
    
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
        self.startupQueue.put({'message': 'KEYS',
                               '__waiting': ScraperThread.ContactKeysVal})
        contactKeys = getContactKeys(get_credentials_method)
        self.startupQueue.put({'progress': 1,
                               '__ready': ScraperThread.ContactKeysVal,
                               '__waiting': ScraperThread.DirectoryKeysVal})
        directoryKeys = getAgencyDirKeys(get_credentials_method)
        self.startupQueue.put({'progress': 2,
                               '__ready': ScraperThread.DirectoryKeysVal})
        print('')

        # Get contact and orginization website data and structure with collected headings
        print('RECORDS')
        self.startupQueue.put({'message': 'RECORDS',
                               '__waiting': ScraperThread.ContactRecordsVal})
        contactRecords = [sheetRecord(row, contactKeys) for row in getContacts(get_credentials_method)]
        self.startupQueue.put({'progress': 3,
                               '__ready': ScraperThread.ContactRecordsVal,
                               '__waiting': ScraperThread.AgencyDirectoryVal})
        self.orgRecords = [sheetRecord(row, directoryKeys) for row in getAgencyDir(get_credentials_method)]
        self.startupQueue.put({'progress': 4,
                               '__ready': ScraperThread.AgencyDirectoryVal})
        print('')

        # Create Dataframes
        self.startupQueue.put({'__waiting': ScraperThread.DataVal})
        cr = pd.DataFrame(contactRecords)
        dr = pd.DataFrame(self.orgRecords)
        print('DATAFRAMES READY') 
        self.startupQueue.put({'message': 'DATAFRAMES READY',
                               'progress': 5,
                               '__ready': ScraperThread.DataVal})
        ## //////////////////  Initialize Contact Checker Classes with Fresh Data  \\\\\\\\\\\\\\\\\\\

        # Setup Contact Record Output
        self.startupQueue.put({'__waiting': ScraperThread.OutputVal})
        cc.ContactSheetOutput.set_output(contactKeys)
        self.startupQueue.put({'progress': 6,
                               '__ready': ScraperThread.OutputVal,
                               '__waiting': ScraperThread.BrowserDriverVal})
        # For this scrape session Give the Verification Handler class an Orgsession with Organization Records
        dm.OrgSession.set_browser_path()                                 ## IMPORTANT STEP: The browser path must be set to the current working directory which varies for different machines
        cc.VerificationHandler.set_orgRecords(dm.HeadlessOrgSession(self.orgRecords))
        self.startupQueue.put({'progress': 7,
                               '__ready': ScraperThread.BrowserDriverVal,
                               '__waiting': ScraperThread.ContactCheckerVal})
        # For this scrape session Give the Verification Handler class the contact record data
        cc.VerificationHandler.set_contactRecords(cr)
        cc.ScrapeSession.set_app_scraper_queue(self.scraperQueue)
        cc.ContactSheetOutput.set_app_scraper_queue(self.scraperQueue)
        cc.ContactCollector.set_app_scraper_queue(self.scraperQueue)
        dm.DirectoryManager.set_app_scraper_queue(self.scraperQueue)
        dm.OrgQuery.set_app_scraper_queue(self.scraperQueue)
        cc.ScrapeSession.set_app_command_queue(self.commandQueue)

        ## Count Rows and Finnish up
        self.startupQueue.put({'rowCounts': {'contact counts': cc.ContactSheetOutput.count_contacts_rows(),
                                             'output counts': cc.ContactSheetOutput.count_scraper_output_rows()}})
        print('CONTACT CHECKER READY')
        print('SCRAPE SESSION OPEN')
        print('')
        self.startupQueue.put({'message': 'SCRAPE SESSION OPEN',
                               'progress': 'FINNISHED',
                               '__ready': ScraperThread.ContactCheckerVal})

            
    def listen_for_cmd(self):
        while True:
            try:
                packet = self.commandQueue.get(0)
                ## Scrape Events
                if 'scrape' in packet:
                    print('The scraper is running')
                    if packet['scrape'] == 'Today':
                        t = cc.ScrapeForToday(self.orgRecords)        
                    elif packet['scrape'] == 'Base':
                        t = cc.ScrapeBase(self.orgRecords)
                    elif packet['scrape'] == 'All':
                        cc.ContactSheetOutput.clear_scraper_output()
                        t = cc.ScrapeAll(self.orgRecords)
                    elif packet['scrape'] == 'Error':
                        cc.ContactSheetOutput.clear_samples()
                        t = cc.ScrapeError(self.orgRecords)
                    
                    ## Count Rows and Finnish up
                    self.scraperQueue.put({'rowCounts': {'contact counts': cc.ContactSheetOutput.count_contacts_rows(),
                                                         'output counts': cc.ContactSheetOutput.count_scraper_output_rows()}})    
                    print('scraper finnished')
                    print('')
                    self.scraperQueue.put({'done':1})
                    return True

                if 'sheet change' in packet:
                    print('Sheet name change for {}'.format(packet['sheet change']))
                    if packet['sheet change'] == 'Today':
                        cc.ContactSheetOutput.change_output_sheet_name('Samples')        
                    elif packet['sheet change'] == 'Base':
                        cc.ContactSheetOutput.change_output_sheet_name('Samples')
                    elif packet['sheet change'] == 'All':
                        cc.ContactSheetOutput.change_output_sheet_name('Scraper Output')
                    elif packet['sheet change'] == 'Error':
                        cc.ContactSheetOutput.change_output_sheet_name('Samples')

                if 'restore' in packet:
                    cc.ContactSheetOutput.restore_contacts()
                    ## Count Rows and Finnish up
                    self.scraperQueue.put({'rowCounts': {'contact counts': cc.ContactSheetOutput.count_contacts_rows(),
                                                         'output counts': cc.ContactSheetOutput.count_scraper_output_rows()}})    
                    self.scraperQueue.put({'done': 1})
                    print("RESTORE COMPLETE")

                if 'transfer' in packet:
                    cc.ContactSheetOutput.transfer_contacts()
                    ## Count Rows and Finnish up
                    self.scraperQueue.put({'rowCounts': {'contact counts': cc.ContactSheetOutput.count_contacts_rows(),
                                                         'output counts': cc.ContactSheetOutput.count_scraper_output_rows()}})    
                    self.scraperQueue.put({'done': 1})
                    print("TRANSFER COMPLETE")
                
                ## Stop Events
                if 'stop' in packet:
                    print('scraper loop done')
                    return False
                
            except queue.Empty:
                time.sleep(.2)