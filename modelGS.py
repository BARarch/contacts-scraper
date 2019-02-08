from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Scraper-Y'

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.NFL-Parse.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        ''' Commented for SheetOutput: No Commandline Args
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
            print("Flags in failed Credential Check: {}".format(flags))
        except ImportError:
        '''
        flags = None
            
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def modelInit():
    ''' Commented for SheetOutput: No Commandline Args
    !! IT WORKS: IN BUISNESS !!
    try:
        import argparse
        print("Trying argParse...")
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        print("Flags in modelInit Check: {}".format(flags))
        
    except ImportError:
    '''
    flags = None
    
    return get_credentials