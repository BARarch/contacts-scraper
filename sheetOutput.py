## Sheet Output Class
''' A general base class for google sheets API input/output
'''
from .modelGS import *

def build_service():
    """Google Sheets API Code.
    """
    credentials = SheetOutput.get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                                discoveryServiceUrl=discoveryUrl)
    return service

def get(SheetId):
    service = build_service()

    request = service.spreadsheets().get(spreadsheetId=SheetId, includeGridData=True)
    result = request.execute()
    return result

def get_properties(SheetId):
    service = build_service()

    request = service.spreadsheets().get(spreadsheetId=SheetId, includeGridData=True, fields='sheets.properties')
    result = request.execute()
    return result

def get_columnMetadata(SheetId):
    service = build_service()

    request = service.spreadsheets().get(spreadsheetId=SheetId, includeGridData=True, fields='sheets.data.columnMetadata')
    result = request.execute()
    return result

class SheetOutput():
    
    get_credentials =  modelInit()
    
    def __init__(self, spreadSheetId, tagName, lastColumn):
        self.service = build_service()
        self.spreadSheetId = spreadSheetId
        self.tagName = tagName
        self.lastColumn = lastColumn
        self.content = self.read_all_rows()

    def read_all_rows(self):
        tabName = self.tagName
        lastColumn = self.lastColumn
        spreadsheetId = self.spreadSheetId
        rangeName = tabName + '!A1:' + lastColumn
        result = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('{} Sheet Rows Collected'.format(str(len(values))))

        return values

    def get_colunm_names(self):
        return self.content[0]

    def get_data(self):
        return self.content[1:]

    def output_single_row(self, row=['Hello', 'World'], rowNum=1):
        spreadsheet_id = self.spreadSheetId
        value_input_option = 'RAW'
        rangeName = self.tagName + '!A' + str(rowNum)
        #print(rangeName)
        values = [row]
        body = {
              'values': values
        }

        try:
            result = self.service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
                                                        valueInputOption=value_input_option, body=body).execute()
        except BaseException as e:
            print('Missed Row Output')
            print(str(e))
            result = e
        else:
            print('Row Written To {}'.format(self.tagName))

        return result 
    
    def output_rows(self, rows, col, rowNumber):
        spreadsheet_id = self.spreadSheetId
        value_input_option = 'RAW'
        rangeName = self.tagName + '!' + col + str(rowNumber)
        values = rows
        body = {
              'values': values
        }

        try:
            result = self.service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
                                                        valueInputOption=value_input_option, body=body).execute()
        except Exception as e:
            print('Missed Row Output')
            print(e)
            return
        else:
            print('{} rows were output to {}'.format(str(len(rows)), self.tagName))

        return result

    def add_sheet(self, sheetTitle='Test'):
        spreadsheet_id = self.spreadSheetId
        body = {
              "requests":   [
                                {
                                    "addSheet": {
                                        "properties": {
                                            "title": sheetTitle,
                                            "tabColor": {
                                                "red": 1.0,
                                                "green": 0.3,
                                                "blue": 0.4
                                                }
                                            }   
                                        }
                                }
                            ]
            }

        try:
            result = self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, 
                                                                 body=body).execute()
        except Exception as e:
            print('New Sheet failed')
            print(e)
            return
        else:
            print('New sheet {} created'.format(sheetTitle))

        return result

       









