print('Testing scraper package installation...')

try:
	print('selenium')	
	import selenium
except:
	print('FAIL: No selenium')
else:
	print('PASS: Version %s \t-3.4.3 works best' % selenium.__version__)


try:
	print('beautifulsoup4')
	import bs4
except:
	print('FAIL: No beatifulsoup4')
else:
	print('PASS: Version %s \t-4.6.0 works best' % bs4.__version__)


try:
	print('time')
	import time
except:
	print('FAIL: No time')
else:
	print('PASS')


try:
	print('datetime')
	import datetime
except:
	print('FAIL: No datetime')
else:
	print('PASS')


try:
	print('pandas')	
	import pandas
except:
	print('FAIL: No pandas')
else:
	print('PASS: Version %s \t-0.20.1 works best' % pandas.__version__)



try:
	print('re')	
	import re
except:
	print('FAIL: No re')
else:
	print('PASS: Version %s \t-2.2.1 works best' % re.__version__)


try:
	print('numpy')	
	import numpy
except:
	print('FAIL: No numpy')
else:
	print('PASS: Version %s \t-1.12.1 works best' % numpy.__version__)

try:
	print('httplib2')	
	import httplib2
except:
	print('FAIL: No httplib2')
else:
	print('PASS: Version %s \t-0.10.3 works best' % httplib2.__version__)


try:
	print('os')
	import os
except:
	print('FAIL: No os')
else:
	print('PASS')


try:
	print('oauth2client')	
	import oauth2client
except:
	print('FAIL: No oauth2client')
else:
	print('PASS: Version %s \t-4.1.2 works best' % oauth2client.__version__)


try:
	print('apiclient')	
	import apiclient
except:
	print('FAIL: No apiclient')
else:
	print('PASS: Version %s \t-1.6.2 works best' % apiclient.__version__)

print('DONE')

