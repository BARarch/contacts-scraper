import scraperModelGS as smgs
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import TimeoutException 
from bs4 import BeautifulSoup

import re

## Classes that are used to Verifiy Contacts on the Association Contacts Directory and Find new ones

class ContactPointerFamily(object):
	##  The goal of this class is to indentify the elements of the DOM tree which represent the name and tittle of a contact
	##  on an organization's aministrative directory page.  Fred is the pointer for the first name, Larry is the pointer for the last
	##  name and in many cases this will be the same element.  When this is the case the Nathan pointer for name points there
	##  as well.  In the case where Fred and Larry are separate elements the nate pointer is used to point to there first common parent.
	##  
	##										Will the real Tom pointer please stand up.
	##
	##  The Tom pointer points to an element which represents the title of the contact.  In many cases this may not be an exact match,
	##  especially when some titles are full sentences.  In indertermining Tom there are many Reggies, elements that are found with at
	##  least one of the words in the listed tittle.  The reggie with the most word that matches becomes Tom. 
	##
	##  The next step is assigning a mother element which is the first common parent of the of the title node (Tom) and name node(s) 
	##  (Nathon or Nate).  She is either Minnie, Martina or the gereral case Mary.  For cituations where the name and title are in the
	##  the same element we assign Mindy as the mother element.  If the first common parent between the name and title is Nate, then
	##  we assign Martina as this Mother element.  However, we are assumming most of these documents are well formatted, and Mary will
	##  point to mother elements that connect distinct name and title elements! 
