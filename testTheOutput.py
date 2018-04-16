import sys
from datetime import datetime
sys.stdout = open('mode.txt', 'w')
print ('Scraper started on ' + datetime.now().strftime('%a, %d %b %Y %H:%M:%S'))
for n in range(5):
	print(n*2)