import scraperModelGS as smgs
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import TimeoutException 
from bs4 import BeautifulSoup

import re

## Classes that are used to Verifiy Contacts on the Association Contacts Directory and Find new ones

class ContactPointerFamily(object):
	
