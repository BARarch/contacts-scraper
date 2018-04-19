import scraperModelGS as smgs

from selenium import webdriver
from selenium.common.exceptions import TimeoutException 
from bs4 import BeautifulSoup

import time
import datetime as dt
import os

import queue
from queryThread import QueryThread


# Company Directory Manager Classes
class DirectoryManager(object):
    ## The goal of this class is to manage the directory in the enviroment not to be one!
    ## the directory as well as it access and packaging functions will opporate as utility functions, these
    ## the routines of this class will call those utility functions
    get_credentials = smgs.modelInit()
    scraperQueue = None

    def __init__(self, orgRecords):
        self.orgRecords = orgRecords
        #self.get_credentials = smgs.modelInit()
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
        
        try:
            timeString = '{} {}'.format(str(row[0][1]), row[0][2])
            print(timeString)
            DirectoryManager.dir_on_with_time('__recordRow', timeString )
        except BaseException as e:
            print(e)


        credentials = DirectoryManager.get_credentials()
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
        DirectoryManager.dir_off('__recordRow')

        return result

    def writeRecordNote(self, note, index):
        """Google Sheets API Code.
        """
        DirectoryManager.dir_on('__recordNote')

        credentials = DirectoryManager.get_credentials()
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
        DirectoryManager.dir_off('__recordNote')
        return result

    @classmethod
    def set_app_scraper_queue(cls, q):
        DirectoryManager.scraperQueue = q

    @classmethod
    def dir_on(cls, place):
        if DirectoryManager.scraperQueue:
            DirectoryManager.scraperQueue.put({'__DIRON': place})

    @classmethod
    def dir_on_with_time(cls, place, timeString):
        if DirectoryManager.scraperQueue:
            DirectoryManager.scraperQueue.put({'__DIRON': place,
                                               'time': timeString})

    @classmethod
    def dir_off(cls, place):
        if DirectoryManager.scraperQueue:
            DirectoryManager.scraperQueue.put({'__DIROFF': place})

    @classmethod
    def change_on(cls, place):
        if DirectoryManager.scraperQueue:
            DirectoryManager.scraperQueue.put({'__NEWBROWSERON': place})

    @classmethod
    def change_off(cls, place):
        if DirectoryManager.scraperQueue:
            DirectoryManager.scraperQueue.put({'__NEWBROWSEROFF': place})

class OrgSession(DirectoryManager):
    browserPath = '/Users/Anthony/scripts/Contacts-Scraper/Drivers/chromedriver' # change path as needed 

    MillisecondFormatMax = 2
    PageLoadTimeout = 20
    ScriptLoadTimeout = 20

    def __init__(self, orgRecords):
        DirectoryManager.__init__(self, orgRecords)

        
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
        if self.anyQueryTimeouts():     #There is a timeout
            print('OrgSession wants new Browser')
            self.new_browser()      #Get a new brower
            self.serialSessionNote('Timed Out')     #Send a Note
            self.sessionStatus = 'Bad'      #Set session Status to bad
            return[self.orgQueries[-1].get_callTimeStr(), '--', '--', self.sessionStatus]
        elif self.anyOtherQueryExceptions():    #There are other exceptions
            self.serialSessionNote('There is either bad source or bad parsing on doc')  #Send a Note
            self.sessionStatus = 'Bad'      #Set session Status to bad
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


    def new_browser(self):
        print('Where is the new browser')

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

    def close_session_browser(self):
        pass

    @classmethod
    def set_browser_path(cls):
        homeDir = os.getcwd()
        intDir =  os.path.join(homeDir, 'Drivers')
        OrgSession.browserPath = os.path.join(intDir, 'chromedriver')

class HeadlessOrgSession(OrgSession):
    ImplicitWait = 25
    PageLoadTimeout = 20
    def __init__(self, orgRecords):
        OrgSession.__init__(self, orgRecords)
        self.sessionBrowser = webdriver.PhantomJS()
        self.sessionBrowser.set_window_size(1600, 1600)
        self.sessionBrowser.implicitly_wait(HeadlessOrgSession.ImplicitWait)
        self.sessionBrowser.set_page_load_timeout(HeadlessOrgSession.PageLoadTimeout)
        print()
        print('Started Headless Browser')
        
    def new_browser(self):
        try:
            DirectoryManager.change_on('HeadlessOrgSession')                                ## If the browser was closed by another user this will fail
            self.sessionBrowser.quit()
        except:
            print('Missing Browser, We will resume')
        else:
            print('HeadLess Browser Closed')
        finally:                            ## So we catch it here
            self.sessionBrowser = webdriver.PhantomJS()
            self.sessionBrowser.set_window_size(1600, 1600)
            self.sessionBrowser.implicitly_wait(HeadlessOrgSession.ImplicitWait)
            self.sessionBrowser.set_page_load_timeout(HeadlessOrgSession.PageLoadTimeout)
            DirectoryManager.change_off('HeadlessOrgSession')
            print('Started NEW Headless Browser')

    def close_session_browser(self):
        self.sessionBrowser.quit()
        
class HeadOrgSession(OrgSession):
    def __init__(self, orgRecords):
        OrgSession.__init__(self, orgRecords)
        self.sessionBrowser = webdriver.Chrome(OrgSession.browserPath)
        self.sessionBrowser.set_page_load_timeout(OrgSession.PageLoadTimeout)
        self.sessionBrowser.set_script_timeout(OrgSession.ScriptLoadTimeout)
        
    def new_browser(self):
        try:                                ## If the browser was closed by another user this will fail
            self.sessionBrowser.close()
        except:
            print('Missing Browser, We will resume')
        finally:                            ## So we catch it here
            self.sessionBrowser = webdriver.Chrome(OrgSession.browserPath)
            self.sessionBrowser.set_page_load_timeout(OrgSession.PageLoadTimeout)
            self.sessionBrowser.set_script_timeout(OrgSession.ScriptLoadTimeout)

    def close_session_browser(self):
            self.sessionBrowser.close()
            
class BatchSessionPing(HeadOrgSession):
    def __init__(self, orgRecords):
        OrgSession.__init__(self, orgRecords)
        for org in DirectoryManager.get_organizations(self):
            try:
                q = OrgSession.processSession(self, org)
            except:
                OrgSession.organizationSessionNote(self, org, "Something Happend Here")
                print('BatchSessionPing wants new Browser')
                OrgSession.new_browser(self)

        


class OrgQuery(object):
    stripped_characters = ['\n', '\r', '\t', '\xa0']
    scraperQueue = None

    def __init__(self, link, browser):
        self.link = link
        try:
            OrgQuery.request_on(self.link)
            start = time.clock()
            self.query = browser.get(link)
            self.responseTime = time.clock() - start
        except TimeoutException:
            self.timeOut = True
            OrgQuery.request_off('Timed out')
        else:
            self.timeOut = False
            OrgQuery.request_off(self.link)

        try:
            self.pageSource = browser.page_source
        except:
            self.sourceError = True
            print("Source Error Here")
        else:
            self.sourceError = False

        try:
            self.soup = BeautifulSoup(OrgQuery.strip_html_junk(self.pageSource), 'lxml')
        except Exception as e:
            self.soupError = True
            print("BeautifulSoup Error Here")
            print(e)
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

    @staticmethod
    def strip_html_junk(str):
        slashed = str
        for c in OrgQuery.stripped_characters:
            slashed = slashed.replace(c, ' ')

        return slashed

    @classmethod
    def set_app_scraper_queue(cls, q):
        OrgQuery.scraperQueue = q

    @classmethod
    def request_on(cls, place):
        if OrgQuery.scraperQueue:
            OrgQuery.scraperQueue.put({'__REQUESTON': place})

    @classmethod
    def request_off(cls, place):
        if OrgQuery.scraperQueue:
            OrgQuery.scraperQueue.put({'__REQUESTOFF': place})

class OrgQueryThread(OrgQuery):
    ThreadTimeOut = 40

    def __init__(self, link, browser):
        self.link = link
        self.responseQueue = queue.Queue()
        self.queryProcess = QueryThread(link, browser, self.responseQueue)

        try:
            OrgQuery.request_on(self.link)
            self.queryProcess.start()                       # Here we start query thread
            cycles = 0
            while True:                                     # Check for response
                try:            
                    time.sleep(1)
                    packet = self.responseQueue.get(False)
                    print()
                except queue.Empty:
                    cycles += 1
                    print('.', end='', flush=True)
                    if cycles > OrgQueryThread.ThreadTimeOut:              # if there is not a timely response
                        # Timeout Condition
                        self.timeOut = True
                        OrgQuery.request_off('Timed out')
                        print('Query Thread Timeout')
                        break
                else:                                       #if there is a response,
                    self.query = packet['query']
                    self.responseTime = packet['response time']
                    break

            
        except TimeoutException:
            self.timeOut = True
            OrgQuery.request_off('Timed out')
        else:
            self.timeOut = False
            OrgQuery.request_off(self.link)

        try:
            self.pageSource = browser.page_source
        except:
            self.sourceError = True
            print("Source Error Here")
        else:
            self.sourceError = False

        try:
            self.soup = BeautifulSoup(OrgQuery.strip_html_junk(self.pageSource), 'lxml')
        except Exception as e:
            self.soupError = True
            print("BeautifulSoup Error Here")
            print(e)
        else:
            self.soupError = False

        self.callTime = dt.datetime.now()


    