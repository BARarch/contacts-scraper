import pandas as pd
import scraperModelGS as smgs

from selenium import webdriver
from selenium.common.exceptions import TimeoutException 
from bs4 import BeautifulSoup

import time
import datetime as dt

def getContacts():
    """Google Sheets API Code.
    Pulls urls for all NFL Team RSS Feeds
    https://docs.google.com/spreadsheets/d/1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs/
    """
    credentials = get_credentials()
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
        print('No data found.')
    else:
        print('Done')

    return values

def getContactKeys():
    """Google Sheets API Code.
    Pulls urls for all NFL Team RSS Feeds
    https://docs.google.com/spreadsheets/d/1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs/
    """
    credentials = get_credentials()
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
        print('No data found.')
    else:
        print('Done')

    return values[0]

def getAgencyDir():
    """Google Sheets API Code.
    Pulls urls for all NFL Team RSS Feeds
    https://docs.google.com/spreadsheets/d/1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs/
    """
    credentials = get_credentials()
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
        print('No data found.')
    else:
        print('Done')

    return values

def getAgencyDirKeys():
    """Google Sheets API Code.
    Pulls urls for all NFL Team RSS Feeds
    https://docs.google.com/spreadsheets/d/1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs/
    """
    credentials = get_credentials()
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
        print('No data found.')
    else:
        print('Done')

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


# Company Directory Manager Classes
class DirectoryManager(object):
	## The goal of this class is to manage the directory in the enviroment not to be one!
	## the directory as well as it access and packaging functions will opporate as utility functions, these
	## the routines of this class will call those utility functions
	def __init__(self, orgRecords):
	    self.orgRecords = orgRecords
	    #self.browser = webdriver.Chrome(path_to_chromedriver)
	    
	def findOrgRecord(self, organization):
	    for org in self.orgRecords:
	        if organization == org['Organization']:
	            return org
	        
	def get_organizations(self):
	    return [x['Organization'] for x in self.orgRecords]
	        
	def orgRecordIndex(self, orgRecord):
	    return self.orgRecords.index(orgRecord)

	def linkList(self, orgRecord):
	    lis = [orgRecord['Directory link'], orgRecord['Link 2'], orgRecord['Link 3'], orgRecord['Link 4']]
	    return lis[:lis.index('')]

	def writeRecordRow(self, row, index):
		"""Google Sheets API Code.
		"""
		credentials = get_credentials()
		http = credentials.authorize(smgs.httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
		                'version=v4')
		service = smgs.discovery.build('sheets', 'v4', http=http,
		                          discoveryServiceUrl=discoveryUrl)

		spreadsheet_id = '1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs'
		value_input_option = 'RAW'
		rangeName = 'Org Leadership Websites!F' + str(index + 2)
		values = row
		body = {
		      'values': values
		}

		result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
		                                                valueInputOption=value_input_option, body=body).execute()

		return result

	def writeRecordNote(self, note, index):
		"""Google Sheets API Code.
		"""
		credentials = get_credentials()
		http = credentials.authorize(smgs.httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
		                'version=v4')
		service = smgs.discovery.build('sheets', 'v4', http=http,
		                          discoveryServiceUrl=discoveryUrl)

		spreadsheet_id = '1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs'
		value_input_option = 'RAW'
		rangeName = 'Org Leadership Websites!J' + str(index + 2)
		values = [[note]]
		body = {
		      'values': values
		}

		result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
		                                                valueInputOption=value_input_option, body=body).execute()

		return result
    

class OrgSession(DirectoryManager):
	chromeBrowserPath = '/Users/Anthony/scripts/Contacts-Scraper/Drivers/chromedriver' # change path as needed 

	MillisecondFormatMax = 2
	PageLoadTimeout = 20
	ScriptLoadTimeout = 20

	def __init__(self, orgRecords):
		DirectoryManager.__init__(self, orgRecords)
		self.sessionBrowser = webdriver.Chrome(OrgSession.chromeBrowserPath)
		self.sessionBrowser.set_page_load_timeout(OrgSession.PageLoadTimeout)
		self.sessionBrowser.set_script_timeout(OrgSession.ScriptLoadTimeout)
        
	def processSession(self, organization):
		self.organization = organization
		self.orgRecord = DirectoryManager.findOrgRecord(self, self.organization)
		self.sessionIndex = DirectoryManager.orgRecordIndex(self, self.orgRecord)

		## Get all links for Session Instance
		self.links = DirectoryManager.linkList(self, self.orgRecord)

		## Retreve Queries
		self.orgQueries = [OrgQuery(link, self.sessionBrowser) for link in self.links]
		    
		## Analyze Query Session Collect Data
		reportRow = self.orgSessionStatusCheck()


		res = DirectoryManager.writeRecordRow(self, [reportRow], self.sessionIndex)

		## Return Query Objects
		return self.orgQueries

	def orgSessionStatusCheck(self):
		# Documents performance and exceptions
		if self.anyQueryTimeouts():		#There is a timeout
			self.new_Browser()		#Get a new brower
			self.serialSessionNote('We have a timeout')		#Send a Note
			self.sessionStatus = 'Bad'		#Set session Status to bad
			return[self.orgQueries[-1].get_callTimeStr(), '--', '--', self.sessionStatus]
		elif self.anyOtherQueryExceptions():	#There are other exceptions
			self.serialSessionNote('There is either bad source or bad parsing on doc')	#Send a Note
			self.sessionStatus = 'Bad'		#Set session Status to bad
			return[self.orgQueries[-1].get_callTimeStr(), '--', '--', self.sessionStatus]

		totalTime = sum([query.get_responseTime() for query in self.orgQueries])
		self.sessionStatus = 'Good'
		self.serialSessionEraseNote()  # For good Session Erase whever note is there

		## Set Response time in Second or Millisecond format
		if totalTime < OrgSession.MillisecondFormatMax:
			timeUnit = 'ms'
			totalTimeFormat = '%.0f' % (totalTime * 1000)
		else:
			timeUnit = 's'
			totalTimeFormat = '%.3f' % totalTime

		return [self.orgQueries[-1].get_callTimeStr() , totalTimeFormat, timeUnit, self.sessionStatus]

	def anyQueryTimeouts(self):
		for query in self.orgQueries:
			if query.timed_out():
				return True
		return False

	def anyOtherQueryExceptions(self):
		for query in self.orgQueries:
			if query.source_bad() or query.soup_bad():
				return True
		return False


	def new_Browser(self):
		try:								## If the browser was closed by another user this will fail
			self.sessionBrowser.close()
		finally:							## So we catch it here
			self.sessionBrowser = webdriver.Chrome(OrgSession.chromeBrowserPath)
			self.sessionBrowser.set_page_load_timeout(OrgSession.PageLoadTimeout)
			self.sessionBrowser.set_script_timeout(OrgSession.ScriptLoadTimeout)


	def serialSessionNote(self, note):
		## Write a note to the organization row of the previous session
		return DirectoryManager.writeRecordNote(self, note, self.sessionIndex)	

	def serialSessionEraseNote(self):
		## Write a note to the organization row of the previous session
		return DirectoryManager.writeRecordNote(self, '', self.sessionIndex)

	def organizationSessionNote(self, organization, note):
		orgRecord = DirectoryManager.findOrgRecord(self, organization)
		index = DirectoryManager.orgRecordIndex(self, orgRecord)
		return DirectoryManager.writeRecordNote(self, note, index)

class BatchSessionPing(OrgSession):
	def __init__(self, orgRecords):
		OrgSession.__init__(self, orgRecords)
		for org in DirectoryManager.get_organizations(self):
			try:
				q = OrgSession.processSession(self, org)
			except:
				OrgSession.organizationSessionNote(self, org, "Something Happend Here")
				OrgSession.new_Browser(self)

		


class OrgQuery(object):
	def __init__(self, link, browser):
		self.link = link
		try:
			start = time.clock()
			self.query = browser.get(link)
			self.responseTime = time.clock() - start
		except TimeoutException:
			self.timeOut = True
		else:
			self.timeOut = False

		try:
			self.pageSource = browser.page_source
		except:
			self.sourceError = True
		else:
			self.sourceError = False

		try:
			self.soup = BeautifulSoup(self.pageSource, 'lxml')
		except:
			self.soupError = True
		else:
			self.soupError = False

		self.callTime = dt.datetime.now()

	def get_query(self):
		return self.query

	def get_pageSource(self):
		return self.pageSource

	def get_soup(self):
		return self.soup

	def get_responseTime(self):
		return self.responseTime

	def get_callTime(self):
		return self.callTime

	def get_callTimeStr(self):
		return self.callTime.strftime('%a %b %d, %Y  %H:%M:%S')

	def timed_out(self):
		return self.timeOut

	def source_bad(self):
		return self.sourceError

	def soup_bad(self):
		return self.soupError
        




if __name__ == '__main__':
	# Initialize Google Sheets for Write
	get_credentials = smgs.modelInit()

	# Get Headers from google sheets
	contactKeys = getContactKeys()
	directoryKeys = getAgencyDirKeys()
	print('KEYS')

	# Get contact and orginization website data and structure with collected headings
	contactRecords = [sheetRecord(row, contactKeys) for row in getContacts()]
	orgRecords = [sheetRecord(row, directoryKeys) for row in getAgencyDir()]
	print('RECORDS COLLECTED')

	# Create Dataframes
	cr = pd.DataFrame(contactRecords)
	dr = pd.DataFrame(orgRecords)
	print('DATAFRAMES READY')




	
