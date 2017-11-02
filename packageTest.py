print('Testing scraper package installation...')

try:
	print('\nselenium')	
	import selenium
except:
	print('FAIL: No selenium')
else:
	print('PASS: Version %s \t\t-3.4.3 works best' % selenium.__version__)


try:
	print('\nbeautifulsoup4')
	import bs4
except:
	print('FAIL: No beatifulsoup4')
else:
	print('PASS: Version %s \t\t-4.6.0 works best' % bs4.__version__)


try:
	print('\ntime')
	import time
except:
	print('FAIL: No time')
else:
	print('PASS')


try:
	print('\ndatetime')
	import datetime
except:
	print('FAIL: No datetime')
else:
	print('PASS')


try:
	print('\npandas')	
	import pandas
except:
	print('FAIL: No pandas')
else:
	print('PASS: Version %s \t\t-0.20.1 works best' % pandas.__version__)



try:
	print('\nre')	
	import re
except:
	print('FAIL: No re')
else:
	print('PASS: Version %s \t\t-2.2.1 works best' % re.__version__)


try:
	print('\nnumpy')	
	import numpy
except:
	print('FAIL: No numpy')
else:
	print('PASS: Version %s \t\t-1.12.1 works best' % numpy.__version__)

try:
	print('\nhttplib2')	
	import httplib2
except:
	print('FAIL: No httplib2')
else:
	print('PASS: Version %s \t\t-0.10.3 works best' % httplib2.__version__)


try:
	print('\nos')
	import os
except:
	print('FAIL: No os')
else:
	print('PASS')


try:
	print('\noauth2client')	
	import oauth2client
except:
	print('FAIL: No oauth2client')
else:
	print('PASS: Version %s \t\t-4.1.2 works best' % oauth2client.__version__)


try:
	print('\napiclient')	
	import apiclient
except:
	print('FAIL: No apiclient')
else:
	print('PASS: Version %s \t\t-1.6.2 works best' % apiclient.__version__)

print('\nDONE')

