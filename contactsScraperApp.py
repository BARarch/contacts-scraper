import pandas as pd
import scraperModelGS as smgs

import directoryManager as dm
import contactChecker as cc

import sys
import time
from tkinter import *
import tkinter.ttk as ttk

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
        self.create_widgets()
        
    def create_widgets(self):
        self.QUIT = Button(self)
        self.QUIT['text'] = "QUIT"
        self.QUIT['fg'] = "red"
        self.QUIT['command'] = self.quit
        self.QUIT.pack({"side": "left"})
        
        self.scrape = Button(self)
        self.scrape['text'] = "Scrape"
        self.scrape['fg'] = "green"
        self.scrape['command'] = self.move_progress
        self.scrape.pack({"side": "left"})
        
        self.pb = ttk.Progressbar(self, orient='horizontal', length=400, mode='determinate')
        self.pb["maximum"] = 200
        self.pb.pack({'side':'right'})
        
    def move_progress(self):
        for i in range(20):
            self.pb.step()
            self.update()
            time.sleep(.02)

    def startup(self):
        # Initialize Google Sheets for Write
        get_credentials_method = smgs.modelInit()

        # Get Headers from google sheets
        print('KEYS')
        contactKeys = getContactKeys(get_credentials_method)
        directoryKeys = getAgencyDirKeys(get_credentials_method)
        print('')

        # Get contact and orginization website data and structure with collected headings
        print('RECORDS')
        contactRecords = [sheetRecord(row, contactKeys) for row in getContacts(get_credentials_method)]
        orgRecords = [sheetRecord(row, directoryKeys) for row in getAgencyDir(get_credentials_method)]
        print('')

        # Create Dataframes
        cr = pd.DataFrame(contactRecords)
        dr = pd.DataFrame(orgRecords)
        print('DATAFRAMES READY')

        ## //////////////////  Initialize Contact Checker Classes with Fresh Data  \\\\\\\\\\\\\\\\\\\

        # Setup Contact Record Output
        cc.ContactSheetOutput.set_output(contactKeys)

        # For this scrape session Give the Verification Handler class an Orgsession with Organization Records
        dm.OrgSession.set_browser_path()                                 ## IMPORTANT STEP: The browser path must be set to the current working directory which varies for different machines
        cc.VerificationHandler.set_orgRecords(dm.HeadlessOrgSession(orgRecords))

        # For this scrape session Give the Verification Handler class the contact record data
        cc.VerificationHandler.set_contactRecords(cr)
        print('CONTACT CHECKER READY')

        ## //////////////////        Scrape Base Case and Turn Off Browser         \\\\\\\\\\\\\\\\\\\

        print('SCRAPE SESSION OPEN')
        

if __name__ == '__main__':
    
    root = Tk()
    app = Application(master=root)
    app.after(500, app.startup)
    app.mainloop()
    root.destroy()
    
   
    
    



	





	
