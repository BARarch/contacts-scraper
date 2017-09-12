import scraperModelGS as smgs


get_credentials = smgs.modelInit()

def getFeeds():
    """Google Sheets API Code.
    Pulls urls for all NFL Team RSS Feeds
    https://docs.google.com/spreadsheets/d/1DUBb9OG1A1Xs6v2PK9Oislz4384DSu2MzEbH8dK0ad4/edit#gid=0
    """
    credentials = get_credentials()
    http = credentials.authorize(smgs.httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = smgs.discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    #specify sheetID and range
    spreadsheetId = '1DUBb9OG1A1Xs6v2PK9Oislz4384DSu2MzEbH8dK0ad4'
    rangeName = 'Sheet1!A2:E'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Done')

    return values

vals = getFeeds()