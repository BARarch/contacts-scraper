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

	docSoup = None

	def __init__(self, rec):
		self.rec = rec
		self.contactPointers = {}

		# Set Regex for First Name, Last Name, and Title
		self.firstNameReg = re.compile('^.*%s.*$' % self.rec['First Name'].to_string(index=False))
		self.lastNameReg = re.compile('^.*%s.*$' % self.rec['Last Name'].to_string(index=False))
		self.titleReg = re.compile('^.*%s.*$' % self.rec['Title'].to_string(index=False))

		# Find Fred and Larry, Elements in tree that match text for first name and last name
		fred = ContactPointerFamily.docSoup.findAll(text=firstNameReg)
		larry = ContactPointerFamily.docSoup.findAll(text=lastNameReg)

		try:
			self.contactPointers['fred'] = fred[0]
		except:
			print('No Fred')

		try:
			self.contactPointers['larry'] = larry[0]
		except:
			print('No Larry')

		# Evaluate a bunch of Reggies to find the one that is Tom.  This code matches elements Word for Word to 
		# identify the title element
		titleWords = self.rec['Title'].to_string(index=False).split()

		reggieCounts = {}

		for t in titleWords:
			wordReg = re.compile('^.*%s.*$' % t)
			reggies = namicSoup.findAll(text=wordReg)
			for reggie in reggies:
				if reggie in reggieCounts:
					reggieCounts[reggie] += 1
				else:
					reggieCounts[reggie] = 1
			# print(t+': '+str(reggies))

		reggieMax = list(reggieCounts.keys())[0]

		for reggie in reggieCounts:
			if reggieCounts[reggie] > reggieCounts[reggieMax]:
				reggieMax = reggie

		self.contactPointers['tom'] = reggieMax

		# Find Nathon or Nate
		if self.contactPointers['fred'] is self.contactPointers['larry']:
			## Most Name Pointers will be nathan(s) because the first and last name of a contact will be in the same element
			self.contactPointers['nathan'] = self.contactPointers['fred']
		else:
			self.contactPointers['nate'] = ContactPointerFamily.commonParent(self.contactPointers['fred'], self.contactPointers['larry']

		## Assign Find Mother Element shes either Mindy, Martina, or the general case Mary
		if 'nathan' in self.contactPointers:
			if self.contactPointers['nathan'] is self.contactPointers['tom']:
				## Mindy: All in one
				self.contactPointers['mindy'] = self.contactPointers['nathan']
			else:
				## Mary: the General Case
				self.contactPointers['mary'] = ContactPointerFamily.commonParent(self.contactPointers['nathan'], self.contactPointers['tom'])

		elif 'nate' in self.contactPointers:
			tomsCommonParent = ContactPointerFamily.commonParent(self.contactPointers['nate'], self.contactPointer['tom'])
			if tomsCommonParent is self.contactPointers['nate']:
				## Martina: nate is toms parent too
				self.contactPointers['martina'] = tomsCommonParent
				
			else:
				## Mary: again, the General Case
				self.contactPointers['mary'] = tomsCommonParent



	@staticmethod
	def commonParent(A,B):
		#step 1 A to B's Parents
	    bParents = B.find_parents()
		if A in bParents:
	    	return A

		#step 2 B to A's Parents
		aParents = A.find_parents()
		if B in aParents:
	    	return B

		Parent_of_b = B.parents
		Parent_of_a = A.parents

		#Step 3 Find Firstof A's ancestors to match in B's
		aFirstCommonParent = next(Parent_of_a)
		while aFirstCommonParent not in bParents:
	    	aFirstCommonParent = next(Parent_of_a)

		#Step 4 Find of First of B's ancestors to match in A's
		bFirstCommonParent = next(Parent_of_b)
		while bFirstCommonParent not in aParents:
	    	bFirstCommonParent = next(Parent_of_b)

		#Step 5 do they match    
		if bFirstCommonParent is aFirstCommonParent:
	    	return bFirstCommonParent
		else:
	    	return None 

	@classmethod
	def set_soup(cls, soup):
		ContactPointerFamily.docSoup = soup


