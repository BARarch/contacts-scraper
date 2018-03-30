import scraperModelGS as smgs
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import TimeoutException 
from bs4 import BeautifulSoup

import re

import numpy as np
from bs4.element import NavigableString

import datetime as dt

import queue










## Classes that are used to Verifiy Contacts on the Association Contacts Directory and Find new ones

class ContactPointerFamily(object):
    ##  The goal of this class is to indentify the elements of the DOM tree which represent the name and tittle of a contact
    ##  on an organization's aministrative directory page.  Fred is the pointer for the first name, Larry is the pointer for the last
    ##  name and in many cases this will be the same element.  When this is the case the Nathan pointer for name points there
    ##  as well.  In the case where Fred and Larry are separate elements the nate pointer is used to point to there first common parent.
    ##  
    ##                                      Will the real Tom pointer please stand up.
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
        self.reggieCounts = {}
        self.noReggies = 0

        # Set Regex for First Name, Last Name, and Title
        self.firstNameReg = re.compile('^.*%s.*$' % self.rec['First Name'].to_string(index=False))
        self.lastNameReg = re.compile('^.*%s.*$' % self.rec['Last Name'].to_string(index=False))
        self.titleReg = re.compile('^.*%s.*$' % self.rec['Title'].to_string(index=False))

        # Find Fred and Larry, Elements in tree that match text for first name and last name
        freds = ContactPointerFamily.docSoup.findAll(text=self.firstNameReg)
        larries = ContactPointerFamily.docSoup.findAll(text=self.lastNameReg)

        try:
            self.contactPointers['fred'] = freds[0]
        except:
            print('No Fred')
            return

        # Filter out matches in Script Tags
        for fred in freds:
            if fred.parent.name == 'script':
                continue
            else:
                self.contactPointers['fred'] = fred
                break

        try:
            self.contactPointers['larry'] = larries[0]
        except:
            print('No Larry')
            return

        # Filter out matches in Script Tags
        for larry in larries:
            if larry.parent.name == 'script':
                continue
            else:
                self.contactPointers['larry'] = larry
                break

        # Find Nathon or Nate
        if self.contactPointers['fred'] is self.contactPointers['larry']:
            ## Most Name Pointers will be nathan(s) because the first and last name of a contact will be in the same element
            self.contactPointers['nathan'] = self.contactPointers['fred']
        else:
            self.contactPointers['nate'] = ContactPointerFamily.commonParent(self.contactPointers['fred'], self.contactPointers['larry'])


        # Evaluate a bunch of Reggies to find the one that is Tom.  This code matches elements Word for Word to 
        # identify the title element
        self.titleWords = self.rec['Title'].to_string(index=False).split()

        

        for t in self.titleWords:
            wordReg = re.compile('^.*%s.*$' % t)
            reggies = ContactPointerFamily.docSoup.findAll(text=wordReg)
            for reggie in reggies:
                if reggie in self.reggieCounts:
                    self.reggieCounts[reggie] += 1
                else:
                    self.reggieCounts[reggie] = 1
            # print(t+': '+str(reggies))
        try:    
            reggieMax = list(self.reggieCounts.keys())[0]
        except IndexError:
            print("No Reggies") 
            return

        self.noReggies = len(list(self.reggieCounts.keys()))

        for reggie in self.reggieCounts:
            if self.reggieCounts[reggie] > self.reggieCounts[reggieMax]:
                reggieMax = reggie

        self.contactPointers['tom'] = reggieMax

        ## Assign Find Mother Element shes either Mindy, Martina, or the general case Mary
        if 'nathan' in self.contactPointers:
            if self.contactPointers['nathan'] is self.contactPointers['tom']:
                ## Mindy: All in one
                self.contactPointers['minnie'] = self.contactPointers['nathan']
            else:
                ## Mary: the General Case
                self.contactPointers['mary'] = ContactPointerFamily.commonParent(self.contactPointers['nathan'], self.contactPointers['tom'])

        elif 'nate' in self.contactPointers:
            tomsCommonParent = ContactPointerFamily.commonParent(self.contactPointers['nate'], self.contactPointers['tom'])
            if tomsCommonParent is self.contactPointers['nate']:
                ## Martina: nate is toms parent too
                self.contactPointers['martina'] = tomsCommonParent

            else:
                ## Mary: again, the General Case
                self.contactPointers['mary'] = tomsCommonParent

    def mary_here(self):
        return 'mary' in self.contactPointers

    def minnie_here(self):
        return 'minnie' in self.contactPointers

    def martina_here(self):
        return 'martina' in self.contactPointers

    def nate_here(self):
        return 'nate' in self.contactPointers

    def nathan_here(self):
        return 'nathan' in self.contactPointers

    def tom_here(self):
        return 'tom' in self.contactPointers

    def fred_here(self):
        return 'fred' in self.contactPointers

    def larry_here(self):
        return 'larry' in self.contactPointers

    def get_mary(self):
        if self.mary_here():
            return self.contactPointers['mary']
        else:
            return None

    def get_minnie(self):
        if self.minnie_here():
            return self.contactPointers['minnie']
        else:
            return None

    def get_martina(self):
        if self.martina_here():
            return self.contactPointers['martina']
        else:
            return None

    def get_nate(self):
        if self.nate_here():
            return self.contactPointers['nate']
        else:
            return None

    def get_nathan(self):
        if self.nathan_here():
            return self.contactPointers['nathan']
        else:
            return None

    def get_tom(self):
        if self.tom_here():
            return self.contactPointers['tom']
        else:
            return None

    def get_fred(self):
        if self.fred_here():
            return self.contactPointers['fred']
        else:
            return None

    def get_larry(self):
        if self.larry_here():
            return self.contactPointers['larry']
        else:
            return None


    @classmethod
    def commonParent(cls, A, B):
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

class VerifiedPointer(ContactPointerFamily):

    def __init__(self, rec):
        ContactPointerFamily.__init__(self, rec)
        self.mary = ContactPointerFamily.get_mary(self)
        self.minnie = ContactPointerFamily.get_minnie(self)
        self.martina = ContactPointerFamily.get_martina(self)
        self.nate = ContactPointerFamily.get_nate(self)
        self.nathan = ContactPointerFamily.get_nathan(self)
        self.tom = ContactPointerFamily.get_tom(self)
        self.fred = ContactPointerFamily.get_fred(self)
        self.larry = ContactPointerFamily.get_larry(self)

        self.output = ContactSheetOutput('Pointer For: %s' % self.nathan if self.nathan != None else "Some Contact")

    def get_output_row(self):
        rec = [self.rec[x].to_string(index=False) for x in self.output.get_contact_keys()]
        scrape = ['Fred' if self.fred_here() else 'None',
                 'Larry' if self.larry_here() else 'None',
                 'Nathan' if self.nathan_here() else 'Nate' if self.nate_here() else 'None',
                 self.noReggies,
                 'Tom' if self.tom_here() else 'None',
                 'Mary' if self.mary_here() else 'Minnie' if self.minnie_here() else 'Martina' if self.martina_here() else 'None',
                 'Verified' if self.mary_here() or self.minnie_here() or self.martina_here() else 'Not Verified']
        rec.extend(scrape)
        return rec

    def write_output_row(self):
        return self.output.output_single_row(self.get_output_row())

    def common_parent(self, otherVP):
        return ContactPointerFamily.commonParent(self.get_mother_element(), otherVP.get_mother_element())

    def get_mother_element(self):
        return self.mary or self.minnie or self.martina or None
                















## Contact Verification Classes
    
class VerificationHandler(object):

    orgRecords = None               ## Will be set to an orgsession Object at initalization
    cr = None                       ## Will be set to dataFrame at class initialization

    def __init__(self, org):
        self.organization = org
        
        # Collect Records from contact Records
        self.records = VerificationHandler.cr[VerificationHandler.cr["Account Name"] == self.organization]
        
        # Call the website of the orgnization and set the soup for all Verification Pointers in this Handler
        self.orgQueries = VerificationHandler.orgRecords.processSession(self.organization)
        print(VerificationHandler.orgRecords.orgSessionStatusCheck())
        self.orgSoup = self.orgQueries[0].get_soup()

        ContactPointerFamily.set_soup(self.orgSoup)

        # Take the data and the soup and get contact pointers
        recs = [self.records.iloc[[ind]] for ind in range(len(self.records))]
        self.pointers = [VerifiedPointer(rec) for rec in recs]
        self.output = ContactSheetOutput('Handler for: %s' % self.organization)


    def get_verified_pointers(self):
        return [pointer for pointer in self.pointers if (pointer.mary_here() or pointer.minnie_here() or pointer.martina_here())]

    def write_contact_pointers(self):
        # batch = [cp.get_output_row() for cp in self.pointers]
        self.output.output_batch_row([cp.get_output_row() for cp in self.pointers])

    @classmethod
    def set_orgRecords(cls, orgRecs):
        VerificationHandler.orgRecords = orgRecs

    @classmethod
    def set_contactRecords(cls, contactRecs):
        VerificationHandler.cr = contactRecs

    @classmethod
    def close_browser(cls):
        VerificationHandler.orgRecords.close_session_browser()


class MotherSetVerifier(VerificationHandler):

    def __init__(self, org):
        VerificationHandler.__init__(self, org)
        self.verifiedPointers = VerificationHandler.get_verified_pointers(self)


















## Contact Extraction Classes
class ContactScraperVerifier(MotherSetVerifier):

    noBrowserPings = 0
    browserPingLimit = 8
    currentOrgName = None

    # Termination States for Organizations checked through this class
    nothing_passed_merge = {}
    link_not_open = {}
    not_extracted = {}
    extracted = {}


    def __init__(self, org):
        MotherSetVerifier.__init__(self, org)
        ContactScraperVerifier.increment_browser_pings()
        ContactScraperVerifier.set_current_org_name(org)
        self.vPointers = self.verifiedPointers

        # Setup the NewContactSheetOutput Class for new records- Send it one of the contact records for the organization
        NewContactSheetOutput.set_Org_Fill_In_Fields(self.records.iloc[[0]])

        # Get Grand Mother elements
        self.gmElements, self.grandMotherMatrix = ContactScraperVerifier.getGrandMotherElements(self.vPointers)

        self.noGm = len(self.gmElements)

        if self.noGm == 1: ## Single Grandmother Case
            self.gm = self.gmElements[0]
            self.distinct_gm = ContactScraperVerifier.distinct_gm(self.gm, self.vPointers)
            
            #if ContactScraperVerifier.distinct_gm(self.gm, self.pointers): ## Grandmother is distinct
            ### Extender Model Selection
            #    self.extenders = [Extender(self.gm, vp) for vp in self.pointers]
            #
            #else:  ## GrandMother is not distinct
            #    ## Extender Model Selection
            #    self.extenders = [RocketOnlyExtender(self.gm, vp) for vp in self.pointers]
                
        else:
            ## Extender Model Selection for Multiple GrandMothers
            self.extenders = None
            self.gm = None
            
    @staticmethod
    def getGrandMotherElements(pointers):
        ## Identify Grandmother elements
        gmElements = []
        gmMatrix = []

        for i in range(len(pointers)):
            igmElements = []
            for j in range(i):
                ## Check to see if the Any Mother element is a Big Momma or "Bertha" Element
                if pointers[i].get_mother_element() is pointers[j].get_mother_element():
                    gm = pointers[i].get_mother_element()
                else:
                    gm = pointers[i].common_parent(pointers[j])
                # Append Match to Grand Mother Matrix
                igmElements.append(gm)

                # Check to see if this is a new grand mother element,
                # if so append to the gmElements list of unique grandmother elements 
                if gm not in gmElements:
                    gmElements.append(gm)

            # Append Matrix Row
            gmMatrix.append(igmElements)

        grandMotherMatrix = np.matrix(gmMatrix)
        return (gmElements, grandMotherMatrix)

    @staticmethod
    def distinct_gm(gm, pts):
        if len(pts) == 0:
            return True
        if gm is pts[0].get_mother_element():
            return False
        else:
            return ContactScraperVerifier.distinct_gm(gm, pts[1:])
        
    @classmethod
    def new_browser(cls):
        VerificationHandler.orgRecords.new_Browser()
        ContactScraperVerifier.reset_ping_count()

    @classmethod
    def reset_ping_count(cls):
        ContactScraperVerifier.noBrowserPings = 0

    @classmethod    
    def increment_browser_pings(cls):
        ContactScraperVerifier.noBrowserPings += 1
        if ContactScraperVerifier.noBrowserPings >= ContactScraperVerifier.browserPingLimit:
            ContactScraperVerifier.new_browser()
            
    @classmethod
    def set_current_org_name(cls, org):
        ContactScraperVerifier.currentOrgName = org

    @classmethod
    def add_to_nothing_passed_merge_dict(cls, numStarts):
        ContactScraperVerifier.nothing_passed_merge[ContactScraperVerifier.currentOrgName] = numStarts
        ContactScraperVerifier.remove_all_others('nothing_passed_merge')

    @classmethod
    def add_to_link_not_open_dict(cls, message):
        ContactScraperVerifier.link_not_open[ContactScraperVerifier.currentOrgName] = message
        ContactScraperVerifier.remove_all_others('link_not_open')

    @classmethod
    def add_to_not_extracted_dict(cls, message):
        ContactScraperVerifier.not_extracted[ContactScraperVerifier.currentOrgName] = message
        ContactScraperVerifier.remove_all_others('not_extracted')

    @classmethod
    def add_to_extracted_dict(cls, numRecords):
        ContactScraperVerifier.extracted[ContactScraperVerifier.currentOrgName] = numRecords
        ContactScraperVerifier.remove_all_others('extracted')
        
    @classmethod
    def remove_all_others(cls, listAdded):
        if (listAdded != 'nothing_passed_merge') and (ContactScraperVerifier.currentOrgName in ContactScraperVerifier.nothing_passed_merge):
            del ContactScraperVerifier.nothing_passed_merge[ContactScraperVerifier.currentOrgName]

        if (listAdded != 'link_not_open') and (ContactScraperVerifier.currentOrgName in ContactScraperVerifier.link_not_open):
            del ContactScraperVerifier.link_not_open[ContactScraperVerifier.currentOrgName]

        if (listAdded != 'not_extracted') and (ContactScraperVerifier.currentOrgName in ContactScraperVerifier.not_extracted):
            del ContactScraperVerifier.not_extracted[ContactScraperVerifier.currentOrgName]

        if (listAdded != 'extracted') and (ContactScraperVerifier.currentOrgName in ContactScraperVerifier.extracted):
            del ContactScraperVerifier.extracted[ContactScraperVerifier.currentOrgName]

    @classmethod
    def clear_stats(cls):
        ContactScraperVerifier.nothing_passed_merge = {}
        ContactScraperVerifier.link_not_open = {}
        ContactScraperVerifier.not_extracted = {}
        ContactScraperVerifier.extracted = {}


class ContactCollector(ContactScraperVerifier):

    scraperQueue = None

    def __init__(self, org):

        print('\nScraping %s' % org)

        try:
            ContactScraperVerifier.__init__(self, org)
            self.write_contact_pointers()


        except BaseException as e:  ## TERMINAL STATE IN THIS BLOCK
            ## Link DID NOT Open
            print("Link DID NOT Open Properly")
            print(e)
            self.errorOutput = SurrogateErrorOutput(org)

            ## Reset Browser
            ContactScraperVerifier.new_browser()

            x = self.errorOutput.output_batch_row([[self.records.iloc[[ind]][key].to_string(index=False) for key in self.errorOutput.get_contact_keys()] for ind in range(len(self.records))], 'Link did not open')

            ## \\** TERMINAL STATE NOTE **\\  Make note that for this org that the link did not open
            ContactScraperVerifier.add_to_link_not_open_dict('bummer')

        else:
            try:
                ContactCollector.parse_on()
                if self.noGm == 1:  ## Single Grandmother Case
                    self.c = Processor(self.gm, self.vPointers)
                    ContactCollector.parse_off()
                elif (self.noGm == 0) and (len(self.vPointers) == 1): ## No GrandMother Single Verfied Pointer - Try this!
                    self.c = Processor(self.vPointers[0].get_mother_element().parent, self.vPointers)
                    ContactCollector.parse_off()
                else: ## TERMINAL STATE IN THIS BLOCK
                    print('Not the right number of Grandmothers %s' % str(self.noGm))
                
                    ## \\** TERMINAL STATE NOTE **\\  Make note that for this org that there were not the right number of Grandmas
                    ContactScraperVerifier.add_to_not_extracted_dict('Not the right number of Grandmothers %s' % str(self.noGm))
                    ContactCollector.parse_off('Not the right number of Grandmothers')

            except: ## TERMINAL STATE IN THIS BLOCK
                ## Some Mysterious Extender/ScraperError no Need for serrogate output
                print('Extender/Scraper Error - NO Extenders')
                ContactCollector.parse_off('No Extenders')

                ## \\** TERMINAL STATE NOTE **\\  Make note that for this org that there was an exception in the extraction process
                ContactScraperVerifier.add_to_not_extracted_dict('Extractor exception in extraction process')

    @classmethod
    def set_app_scraper_queue(cls, q):
        ContactCollector.scraperQueue = q

    @classmethod
    def parse_on(cls, place='ContactCollector'):
        if ContactCollector.scraperQueue:
            ContactCollector.scraperQueue.put({'__PARSEON': place})

    @classmethod
    def parse_off(cls, place='ContactCollector'):
        if ContactCollector.scraperQueue:
            ContactCollector.scraperQueue.put({'__PARSEOFF': place})





















## The Dorito and the Chip
class Dorito(object):
    def __init__(self, gm, pointers):
        self.grandMotherElement = gm
        self.verifiedPointers = pointers
        self.scrapePointers = Dorito.filterPointers(pointers)
        self.result = None
        self.finalPointers = MergeSet(pointers)

    def extract(self):
        ## This class will test the first One
        try:
            self.x = Extractor(self.grandMotherElement, self.scrapePointers[0])
            self.result = self.x.get_result_set()
        except IndexError:
            print("No Scrapable Matches")
        
    def merge_result(self):
        if self.result:
            self.finalPointers.merge_pointers(self.result)


            if not str(self.finalPointers):  ##  TERMINAL STATE IN THIS BLOCK 
                print("Nothing passed Merge")
                
                ## \\** TERMINAL STATE NOTE **\\  Make note that for this org nothing passed
                ContactScraperVerifier.add_to_nothing_passed_merge_dict(len(self.result.get_pointers()))
                
                
            else:  ##  TERMINAL STATE IN THIS BLOCK -- SUCCESS!!
                ## \\** TERMINAL STATE NOTE **\\  Make note that for this org that record were collected and passed
                ContactScraperVerifier.add_to_extracted_dict(len(self.finalPointers.get_pointers()))
                
                
        else:  ##  TERMINAL STATE IN THIS BLOCK
            print("Nothing to Merge")

            ## Make note that for this org that there were no results to merge
            ContactScraperVerifier.add_to_nothing_passed_merge_dict('No Results to Merge')

        self.report()
        
    def merge_result_no_report(self):
        if self.result:
            self.finalPointers.merge_pointers(self.result)


            if not str(self.finalPointers):  ##  TERMINAL STATE IN THIS BLOCK
                print("Nothing passed Merge")
            
                ## \\** TERMINAL STATE NOTE **\\  Make note that for this org nothing passed
                ContactScraperVerifier.add_to_nothing_passed_merge_dict(len(self.result.get_pointers()))
            
            
            else:  ##  TERMINAL STATE IN THIS BLOCK -- SUCCESS!!
                ## \\** TERMINAL STATE NOTE **\\  Make note that for this org that record were collected and passed
                ContactScraperVerifier.add_to_extracted_dict(len(self.finalPointers.get_pointers()))
                                                    
        else:  ##  TERMINAL STATE IN THIS BLOCK
            print("Nothing to Merge")

            ## \\** TERMINAL STATE NOTE **\\  Make note that for this org that there were no results to merge
            ContactScraperVerifier.add_to_nothing_passed_merge_dict('No Results to Merge')

            
    def report(self):
        print('Verified Pointers         \t\t\t\t\t\t%s' % len(self.verifiedPointers))
        print('Scrape Pointers           \t\t\t\t\t\t%s' % len(self.scrapePointers))
        print('Start Pointers            \t\t\t\t\t\t%s' % (len(self.result.get_pointers()) if self.result else 0))
        try:
            print('Start Type                \t\t\t\t%s' % self.x.startsType)
            print('Merged (Filtered) Pointers\t\t\t\t\t\t%s' % len(self.finalPointers.get_pointers()))
            print(self.finalPointers)
            
        except AttributeError:
            print('Start Type                \t\t\t\tNO EXTRACTORS')

    def write_contacts(self):
        self.finalPointers.write_new_contacts()

    @staticmethod
    def filterPointers(vps):
        return [pointer for pointer in vps if pointer.mary_here() and pointer.nathan_here]


class RanchDorito(Dorito):
    def __init__(self, gm, pointers):
        Dorito.__init__(self, gm, pointers)
        self.nothingToMerge = True
        self.nothingPassedMerge = True
        self.passedAndExtracted = False

    def extract(self, scrapePointer):
    ## This class will test the scrape pointer passed in
        try:
            self.x = Extractor(self.grandMotherElement, scrapePointer)
            self.result = self.x.get_result_set()
        except IndexError:
            print("No Scrapable Matches")

    def merge_result(self):
        if self.result:
            self.nothingToMerge = False
            len0 = len(self.finalPointers.get_pointers())
            self.finalPointers.merge_pointers(self.result)
            len1 = len(self.finalPointers.get_pointers())

            ## Check to see if the number of final pointers increases due to this merge
            if len0 != len1:
                self.nothingPassedMerge = False
                self.passedAndExtracted = True

            if not str(self.finalPointers):  ##  TERMINAL STATE IN THIS BLOCK
                print("Nothing passed Merge for this Pointer")
  
        else:
            print("Nothing to Merge from this Pointer")





class Chip(Dorito):
    def __init__(self, gm, pointers):
        Dorito.__init__(self, gm, pointers)
        Dorito.extract(self)
        Dorito.merge_result(self)
        Dorito.write_contacts(self)

class Processor(RanchDorito):
    def __init__(self, gm, pointers):
        RanchDorito.__init__(self, gm, pointers)
        self.mergeAttempts = 0
        for sp in self.scrapePointers:
            ## Step1: Extract
            self.result = None
            RanchDorito.extract(self, sp)

            ## Step2: Count Attepts
            if self.result:
                self.mergeAttempts += len(self.result.get_pointers())


            ## Step3: Merge
            RanchDorito.merge_result(self)

        ## Terninal States
        if self.nothingToMerge:
            ContactScraperVerifier.add_to_nothing_passed_merge_dict('No Results to merge')

        elif self.nothingPassedMerge:
            ContactScraperVerifier.add_to_nothing_passed_merge_dict('No Results to merge')

        elif self.passedAndExtracted:
            ContactScraperVerifier.add_to_extracted_dict(len(self.finalPointers.get_pointers()))

        self.report(self.mergeAttempts)
        RanchDorito.write_contacts(self)
        
    def report(self, attempts):
        print('Verified Pointers         \t\t\t\t\t\t%s' % len(self.verifiedPointers))
        print('Scrape Pointers           \t\t\t\t\t\t%s' % len(self.scrapePointers))
        print('Start Pointers            \t\t\t\t\t\t%s' % str(attempts))
        try:
            print('Start Type                \t\t\t\t%s' % self.x.startsType)
            print('Merged (Filtered) Pointers\t\t\t\t\t\t%s' % len(self.finalPointers.get_pointers()))
            print(self.finalPointers)
            
        except AttributeError:
            print('Start Type                \t\t\t\tNO EXTRACTORS')




















## The Extender

class Extender(object):
    def __init__(self, gm, pointer):
        self.gm = gm
        self.vp = pointer

        self.tag_nathans()
        self.tag_toms()

        self.tom_missile = self.mother_to_tom_missile()
        self.tom_rocket = self.nathan_to_tom_rocket()
        self.nathan_shuttle = self.nathan_to_element()

        self.nathan_missile = self.mother_to_nathan_missile()
        self.nathan_rocket = self.tom_to_nathan_rocket()
        self.tom_shuttle = self.tom_to_element()

        #self.reset_tree()
        
    ## Tagging Functions ------------------------------------ 
    ##
    def tag_nathans(self):
        if self.vp.get_mother_element() is self.vp.nathan.parent:  ## Gotta Catch those first elements before the get away
            self.vp.nathan.parent['nathan'] = 0
        else:
            return Extender.parent_cycle_up(self.vp.get_mother_element(), self.vp.nathan.parent, 'nathan', 0)

    def tag_toms(self):
        if self.vp.get_mother_element() is self.vp.tom.parent:  ## Gotta Catch those first elements before the get away
            self.vp.tom.parent['tom'] = 0
        else:
            return Extender.parent_cycle_up(self.vp.get_mother_element(), self.vp.tom.parent, 'tom', 0)

    def reset_tree(self):
        ## Clear all tom, nathan and sib atributes
        for tomTag in self.gm.find_all(Extender.has_tom):
            del tomTag['tom']    
        for nathanTag in self.gm.find_all(Extender.has_nathan):
            del nathanTag['nathan'] 
        for sibTag in self.gm.find_all(Extender.has_sib):
            del sibTag['sib']

    @staticmethod
    def parent_cycle_up(motherElement, element, atr, num):
        ## We tag up THOUGH the MotherELement
        if element is motherElement:
            element[atr] = num
            #element['sib'] = atr
        else:
            element[atr] = num
            return Extender.parent_cycle_up(motherElement, element.parent, atr, num + 1)

    @staticmethod
    def contents_position(elm):
        return Extender.contents_position_loop(elm, 0)

    @staticmethod
    def contents_position_loop(elm, num):
        if len(list(elm.previous_siblings)) == 0:
            return num
        else:
            return Extender.contents_position_loop(elm.previous_sibling, num + 1)

    @staticmethod
    def has_tom(tag):
        try:
            return 'tom' in tag.attrs
        except AttributeError:
            return False

    @staticmethod
    def has_nathan(tag):
        try:
            return 'nathan' in tag.attrs
        except AttributeError:
            return False

    @staticmethod
    def has_sib(tag):
        try:
            return 'sib' in tag.attrs
        except AttributeError:
            return False
        
    @staticmethod
    def check_siblings(sibs, attFunc):
        for sib in sibs:
            if attFunc(sib):
                return True
        return False

    ## Shuttle Functions ------------------------------------
    ##
    def nathan_to_element(self):
        return lambda start: start.contents[Extender.contents_position(self.vp.nathan)]

    def tom_to_element(self):
        return lambda start: start.contents[Extender.contents_position(self.vp.tom)]

    ## Missle Functions ------------------------------------
    ##
    def mother_to_tom_missile(self):
        motherElement = self.vp.get_mother_element()

        if self.vp.tom is motherElement:
            return lambda start: start
        else:
            return lambda start: Extender.cycle_up_mother(self.vp.tom.parent, motherElement, start).contents[Extender.contents_position(self.vp.tom)]

    def mother_to_nathan_missile(self):
        motherElement = self.vp.get_mother_element()

        if self.vp.nathan is motherElement:
            return lambda start: start
        else:
            return lambda start: Extender.cycle_up_mother(self.vp.nathan.parent, motherElement, start).contents[Extender.contents_position(self.vp.nathan)]

    @staticmethod
    def cycle_up_mother(elm, motherElement, start):
        if elm is motherElement:
            return start
        else:
            return Extender.cycle_up_mother(elm.parent, motherElement, start).contents[Extender.contents_position(elm)]


    ## Rocket Functions ------------------------------------
    ##
    def nathan_to_tom_rocket(self):
        ## Compute the route from nathan startnode to tom by starting at tom and recursing up, accross and then down
        ## looing for nathan = 0 attribute

        return lambda start: Extender.cycle_up(self.vp.tom, 'nathan', start)

    def tom_to_nathan_rocket(self):
        ## Compute the route from tom startnode to nathan by starting at nathan and recursing up, accross and then down
        ## looing for tom = 0 attibute

        return lambda start: Extender.cycle_up(self.vp.nathan, 'tom', start)

    @staticmethod
    def cycle_up(elm, to, start):
        ## Set Attribut Search Function
        attrFunc = Extender.has_tom if to == 'tom' else Extender.has_nathan

        ## FIRST check yo'self
        if attrFunc(elm):  ## Switch Direction but don't move
            return Extender.cycle_down(elm, to, start) 
        ## SECOND look Left for shoulder in siblings
        elif Extender.check_siblings(elm.previous_siblings, attrFunc):
            return Extender.cycle_left(elm.previous_sibling, to, start).next_sibling
        ## Then look right
        elif Extender.check_siblings(elm.next_siblings, attrFunc):
            return Extender.cycle_right(elm.next_sibling, to, start).previous_sibling
        ## if nothing here go up
        else:
            return Extender.cycle_up(elm.parent, to, start).contents[Extender.contents_position(elm)]

    @staticmethod
    def cycle_left(elm, to, start):
        attrFunc = Extender.has_tom if to == 'tom' else Extender.has_nathan

        ## if this is the shoulder change functions but dont move
        if attrFunc(elm):
            return Extender.cycle_down(elm, to, start)
        ## if not check the element to the left
        else:
            return Extender.cycle_left(elm.previous_sibling, to, start).next_sibling

    @staticmethod
    def cycle_right(elm, to, start):
        attrFunc = Extender.has_tom if to == 'tom' else Extender.has_nathan

        ## if this is the shoulder change functions but dont move
        if attrFunc(elm):
            return Extender.cycle_down(elm, to, start)
        ## if not check the element to the left
        else:
            return Extender.cycle_right(elm.next_sibling, to, start).previous_sibling

    @staticmethod
    def cycle_down(elm, to, start):
        return Extender.cycle_down_loop(elm[to], start)

    @staticmethod
    def cycle_down_loop(dist, start):
        ## Start Node Condition
        if dist == 0:
            return start
        else: 
            return Extender.cycle_down_loop(dist - 1, start).parent

















## Extractor Classes

class Extractor(Extender):
    nathanStartType = '__nathanStarts__'
    tomStartType = '__tomStarts__'
    motherStartType = '__motherStarts__'

    def __init__(self, gm, pointer):
        Extender.__init__(self, gm, pointer)
        self.startBlock = StartBlockNoMother(gm, pointer)
        self.startsType, self.starts = self.get_starts()
        self.resultSet = NewPointerSet()
        self.test_starts()
        self.reset_tree()
        
    def get_starts(self):
        return self.startBlock.get_optimal_starts()

    def test_starts(self):
        return [self.test_start(self.startsType, st) for st in self.starts]
        
    def test_start(self, startType, start):
        if startType == Extractor.nathanStartType:   ## Nathan Start Case, Nathan Shuttle, Tom Rocket to 
            np = NewPointer(start, self.nathan_shuttle, self.tom_rocket)
            self.resultSet.addPointer(np)
            return np
        if startType == Extractor.tomStartType:   ## Tom Start Case, Tom Shuttle, Nathan Rocket 
            np = NewPointer(start, self.nathan_rocket, self.tom_shuttle)
            self.resultSet.addPointer(np)
            return np
        if startType == Extractor.motherStartType:   ## Mother Start Case, Missile for Missle for Nathan, Missile for Tom 
            np = NewPointer(start, self.nathan_missile, self.tom_missile)
            self.resultSet.addPointer(np)
            return np

    def get_result_set(self):
        return self.resultSet

    def quick_report(self):
        print(str(self.resultSet))


class ExtractorNoMother(Extractor):
    nathanStartType = '__nathanStarts__'
    tomStartType = '__tomStarts__'
    motherStartType = '__motherStarts__'

    def __init__(self, gm, pointer):
        Extractor.__init__(self, gm, pointer)
        self.startBlock = StartBlockNoMother(gm, pointer)
        self.startsType, self.starts = self.get_starts()
        self.reset_tree()
        
    def get_starts(self):
        return self.startBlock.get_optimal_starts()





















## StartBlockClasses

class StartBlock(object):
    def __init__(self, gm, pointer):
        self.vp = pointer
        self.gm = gm

        self.nathanNameStarts = gm.find_all(pointer.nathan.parent.name)
        self.noNathanNameStarts = len(self.nathanNameStarts)
        self.tomNameStarts = gm.find_all(pointer.tom.parent.name)
        self.noTomNameStarts = len(self.tomNameStarts)
        self.motherNameStarts = gm.find_all(pointer.get_mother_element().name)
        self.noMotherNameStarts = len(self.motherNameStarts)

        self.noNathanClasses = self.get_no_nathan_classes()
        self.noTomClasses = self.get_no_tom_classes()
        self.noMotherClasses = self.get_no_mother_classes()
        
    def get_no_nathan_classes(self):
        if 'class' in self.vp.nathan.parent.attrs:
            return len(self.vp.nathan.parent['class'])
        else:
            return 0

    def get_no_tom_classes(self):
        if 'class' in self.vp.tom.parent.attrs:
            return len(self.vp.tom.parent['class'])
        else:
            return 0        

    def get_no_mother_classes(self):
        if 'class' in self.vp.get_mother_element().attrs:
            return len(self.vp.get_mother_element()['class'])
        else:
            return 0
        
    def get_nathan_class_starts(self):
        return self.gm.find_all(class_=self.vp.nathan.parent['class'])

    def get_tom_class_starts(self):
        return self.gm.find_all(class_=self.vp.tom.parent['class'])

    def get_mother_class_starts(self):
        return self.gm.find_all(class_=self.vp.get_mother_element()['class'])

    def get_optimal_starts(self):
        maxNoClasses = max([self.noNathanClasses, self.noTomClasses, self.noMotherClasses])
        minNoNameStarts = min([self.noNathanNameStarts, self.noTomNameStarts, self.noMotherNameStarts])

        #dispatch
        if maxNoClasses > 0: ## There are classes to choose better starts
            if self.noMotherClasses == maxNoClasses:
                return '__motherStarts__', self.get_mother_class_starts()
            elif self.noNathanClasses == maxNoClasses:
                return '__nathanStarts__', self.get_nathan_class_starts()
            else:
                return '__tomStarts__', self.get_tom_class_starts()
        else:  ## There are no classes to test mus go by the minimun number of name matches
            if self.noMotherNameStarts == minNoNameStarts:
                return '__motherStarts__', self.motherNameStarts
            elif self.noNathanNameStarts == minNoNameStarts:
                return '__nathanStarts__', self.nathanNameStarts
            else:
                return '__tomStarts__', self.tomNameStarts


class StartBlockNoMother(StartBlock):
    def __init__(self, gm, pointer):
        StartBlock.__init__(self, gm, pointer)

    def get_optimal_starts(self):
        ## Unlike get_optimal_starts from the inheritted StartBlock this one does not return mother starts
        maxNoClasses = max([self.noNathanClasses, self.noTomClasses])
        minNoNameStarts = min([self.noNathanNameStarts, self.noTomNameStarts])

        #dispatch
        if maxNoClasses > 0: ## There are classes to choose better starts
            if self.noNathanClasses == maxNoClasses:
                return '__nathanStarts__', self.get_nathan_class_starts()
            else:
                return '__tomStarts__', self.get_tom_class_starts()
        else:  ## There are no classes to test mus go by the minimun number of name matches
            if self.noNathanNameStarts == minNoNameStarts:
                return '__nathanStarts__', self.nathanNameStarts
            else:
                return '__tomStarts__', self.tomNameStarts

















## New Pointer Class

class NewPointer(object):
    def __init__(self, start, nathanTest, tomTest):
        self.nathanRoute = nathanTest
        self.tomRoute = tomTest
        self.start = start

        ## Execute Test
        self.nathan = self.test_nathan()
        self.tom = self.test_tom()

        self.output = ContactSheetOutput('New Pointer For: %s start' % str(start))
        
    def test_nathan(self):
        try:
            result = self.nathanRoute(self.start)
            if type(result) is not NavigableString:
                result = None
        except:
            result = None
            
        return result
    
    def test_tom(self):
        try:
            result = self.tomRoute(self.start)
            if type(result) is not NavigableString:
                result = None
        except:
            result = None
            
        return result
    
    def get_tom(self):
        return self.tom
    
    def get_first_last_name(self):
        passes = ['Mr', 'MR', 'Miss', 'Mrs', 'MRS', 'MS', 'Ms', 'Dr']
        nameWords = self.nathan.split(' ')
        spaceFiltered = [word for word in nameWords if word]
        ## loop through name words until you encounter the first two full words that are not passes

        firstNamePt = None
        lastNamePt = None

        for i in range(len(spaceFiltered)):
            if (spaceFiltered[i] not in passes) and ('.' not in spaceFiltered[i]):
                firstNamePt = i
                break

        for j in range(i+1,(len(spaceFiltered))):
            if (spaceFiltered[j] not in passes) and ('.' not in spaceFiltered[j]):
                lastNamePt = j
                break
        try:        
            firstName = ' '.join(spaceFiltered[:firstNamePt + 1])
            lastName = ' '.join(spaceFiltered[lastNamePt:])  
        except TypeError:
            return None, None

        if lastName: ## Last Name was Defined, return Tuple
            return firstName, lastName
        else:        ## Last Name was not Properly Defined result use first Name only
            return firstName, None
        
    def get_clean_tom(self):
        ## Returns a cleaned up version of the title
        tomWords = self.tom.split(' ')
        #filter out spaces
        return ' '.join([word for word in tomWords if word])

    def no_tom_words(self):
        return NewPointer.word_count(self.tom)

    def no_nathan_words(self):
        return NewPointer.word_count(self.nathan)

    def get_output_dict(self):
        outputDict = {}
        outputDict['firstName'], outputDict['lastName'] = self.get_first_last_name()
        outputDict['title'] = self.get_clean_tom()
        return outputDict

    @staticmethod
    def word_count(field):
        ## Returns a cleaned up version of the title
        fieldWords = field.split(' ')
        #filter out spaces
        return len([word for word in fieldWords if word])

    def get_nathan(self):
        return self.nathan























## NewPointerSet and MergeSetClasses

class NewPointerSet(object):
    def __init__(self):
        self.newPointers = []

    def addPointer(self, newPointer):
        self.newPointers.append(newPointer)

    def __str__(self):
        s = ''
        for pt in self.newPointers:
            s += ('%s     as     %s\n' % (str(pt.get_nathan()), str(pt.get_tom())))
        return s

    def get_pointers(self):
        return self.newPointers

class MergeSet(NewPointerSet):
    
    nathanWordLimit = 12
    tomWordLimit = 20

    def __init__(self, vps):
        NewPointerSet.__init__(self)
        self.verifiedPointers = vps
        self.output = NewContactSheetOutput()

    def merge_pointers(self, newPointerSet):
        for np in newPointerSet.get_pointers():
            self.add_pointer(np)

    def add_pointer(self, newPointer):
        ## Pointer has to meet certain conditions to be added to the MergeSet
        if MergeSet.has_a_failed_route(newPointer):
            return False
        if MergeSet.is_nothing(newPointer.tom) or MergeSet.is_nothing(newPointer.nathan):
            return False
        if MergeSet.is_an_email(newPointer.tom) or MergeSet.is_an_email(newPointer.nathan):
            return False
        if MergeSet.is_too_long(newPointer):
            return False
        if MergeSet.fails_name_test(newPointer):
            return False
        if self.a_match_to_verified_pointers(newPointer):
            return False
        if self.a_match_in_set(newPointer):
            return False
        
        ## Add to MergeSetCase
        self.newPointers.append(newPointer)
        
    def write_new_contacts(self):
        self.output.output_batch_row([np.get_output_dict() for np in self.get_pointers()])
        
    @staticmethod
    def fails_name_test(pointer):
        firstName, lastName = pointer.get_first_last_name()
        return not (firstName, lastName)

    @staticmethod
    def is_too_long(pointer):
        if pointer.no_nathan_words() > MergeSet.nathanWordLimit:
            return True
        if pointer.no_tom_words() > MergeSet.tomWordLimit:
            return True
        return False
                                                    
    @staticmethod
    def is_an_email(pointerWord):
        if '@' in pointerWord:
            return True
        return False

    @staticmethod                                                   
    def is_nothing(pointerWord):
        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'       
        for char in pointerWord:
            if char in letters:
                return False
        return True 

    @staticmethod
    def has_a_failed_route(pointer):
        if not pointer.tom:
            return True
        if not pointer.nathan:
            return True
        return False

    def a_match_in_set(self, pointer):
        for np in self.newPointers:
            if pointer.nathan is np.nathan:
                return True
            if pointer.tom is np.tom:
                return True
        return False

    def a_match_to_verified_pointers(self, pointer):
        for vp in self.verifiedPointers:
            if pointer.nathan is vp.nathan:
                return True
            if pointer.tom is vp.tom:
                return True
        return False
























## Sheet Output Classes

class ContactSheetOutput(object):
    get_credentials = smgs.modelInit()
    contactKeys = []   
    initialRead = ""
    initialRow = 7
    currentRow = 7
    outputSheetName = 'Samples'
    scraperQueue = None

    def __init__(self, name):
        self.name = name

    def output_single_row(self, row):
        """Google Sheets API Code.
        """
        ContactSheetOutput.out_on('__singleRow')

        credentials = ContactSheetOutput.get_credentials()
        http = credentials.authorize(smgs.httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = smgs.discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheet_id = '1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs'
        value_input_option = 'RAW'
        rangeName = ContactSheetOutput.outputSheetName + '!A' + str(ContactSheetOutput.currentRow)
        values = [row]
        body = {
              'values': values
        }

        try:
            result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
                                                        valueInputOption=value_input_option, body=body).execute()
        except BaseException as e:
            print('Missed Row Output')
            result = e
        else:
            ContactSheetOutput.currentRow += 1

        ContactSheetOutput.out_off('__singleRow')
        return result 

    def output_batch_row(self, rows):
        """Google Sheets API Code.
        """
        ContactSheetOutput.out_on('__contacts')

        credentials = ContactSheetOutput.get_credentials()
        http = credentials.authorize(smgs.httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = smgs.discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheet_id = '1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs'
        value_input_option = 'RAW'
        rangeName = ContactSheetOutput.outputSheetName + '!A' + str(ContactSheetOutput.currentRow)
        values = rows
        body = {
              'values': values
        }

        try:
            result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
                                                        valueInputOption=value_input_option, body=body).execute()
        except:
            print('Missed Row Output')
        else:
            ContactSheetOutput.currentRow += len(rows)

        ContactSheetOutput.out_off('__contacts')
        return result

    def get_contact_keys(self):
        return ContactSheetOutput.contactKeys   

    @classmethod
    def set_output(cls, keys):
        """Google Sheets API Code.
        Pulls urls for all NFL Team RSS Feeds
        https://docs.google.com/spreadsheets/d/1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs/
        """
        credentials = ContactSheetOutput.get_credentials()
        http = credentials.authorize(smgs.httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = smgs.discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        #specify sheetID and range
        spreadsheetId = '1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs'
        rangeName = ContactSheetOutput.outputSheetName + '!A' + str(ContactSheetOutput.initialRow) + ':N'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])

        if not values:
            print('RECORD OUTPUT READY: No Reocords')
        else:
            print('RECORD OUTPUT READY')
            ContactSheetOutput.initialRead = values
            ContactSheetOutput.currentRow = ContactSheetOutput.initialRow + len(values)

        ContactSheetOutput.contactKeys = keys[:14]  # Changes the 14 to alter the fields from the contacts replicated in the output

    @classmethod
    def change_output_sheet_name(cls, name):
        ContactSheetOutput.outputSheetName = name

    @classmethod
    def set_app_scraper_queue(cls, q):
        ContactSheetOutput.scraperQueue = q

    @classmethod
    def out_on(cls, place):
        if ContactSheetOutput.scraperQueue:
            ContactSheetOutput.scraperQueue.put({'__OUTON': place})

    @classmethod
    def out_off(cls, place):
        if ContactSheetOutput.scraperQueue:
            ContactSheetOutput.scraperQueue.put({'__OUTOFF': place})

       



class NewContactSheetOutput(ContactSheetOutput):
    dummyRecord = None

    def __init__(self):
        ContactSheetOutput.__init__(self, NewContactSheetOutput.dummyRecord['Account Name'].to_string(index=False))
        
    def output_batch_row(self, newContactInfo):
        """Google Sheets API Code.  Since we are in NewContacts Sheet Output, the batch out put function is tasked
           with weaving the information from the new contact with the organization information from the other columns.
           These will be filled in to accompany First Name Last Name and Tittle for the new contacts 
        """
        ContactSheetOutput.out_on('__newContacts')

        credentials = ContactSheetOutput.get_credentials()
        http = credentials.authorize(smgs.httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = smgs.discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheet_id = '1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs'
        value_input_option = 'RAW'
        rangeName = ContactSheetOutput.outputSheetName + '!A' + str(ContactSheetOutput.currentRow)
        values = [NewContactSheetOutput.weaveContactInfo(nci) for nci in newContactInfo]
        body = {
              'values': values
        }

        try:
            result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
                                            valueInputOption=value_input_option, body=body).execute()
        except:
            print('Missed Row Output')
        else:
            ContactSheetOutput.currentRow += len(values)

        ContactSheetOutput.out_off('__newContacts')
        return result

    @staticmethod
    def weaveContactInfo(nci):
        return [NewContactSheetOutput.dummyRecord['Account ID'].to_string(index=False),
                NewContactSheetOutput.dummyRecord['Account Name'].to_string(index=False),
                '',
                nci['firstName'],
                nci['lastName'],
                nci['title'],
                '',
                NewContactSheetOutput.dummyRecord['Mailing Street'].to_string(index=False),
                NewContactSheetOutput.dummyRecord['Mailing City'].to_string(index=False),
                NewContactSheetOutput.dummyRecord['Mailing State/Province'].to_string(index=False),
                NewContactSheetOutput.dummyRecord['Mailing Zip/Postal Code'].to_string(index=False),
                NewContactSheetOutput.dummyRecord['Mailing Country'].to_string(index=False),
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                'New']

    @classmethod
    def set_Org_Fill_In_Fields(cls, record):
        NewContactSheetOutput.dummyRecord = record


class SurrogateErrorOutput(ContactSheetOutput):
    def __init__(self, name):
        ContactSheetOutput.__init__(self, name)

    def output_batch_row(self, rows, errorMessage):
        """Google Sheets API Code. Here at SurrogateErrorOutput we append the error message information to the end of each row 
        """
        ContactSheetOutput.out_on('__error')

        credentials = ContactSheetOutput.get_credentials()
        http = credentials.authorize(smgs.httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = smgs.discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheet_id = '1p1LNyQhNhDBNEOkYQPV9xcNRe60WDlmnuiPp78hxkIs'
        value_input_option = 'RAW'
        rangeName = ContactSheetOutput.outputSheetName + '!A' + str(ContactSheetOutput.currentRow)
        #values = rows
        values = [SurrogateErrorOutput.appendError(row, errorMessage) for row in rows]
        body = {
              'values': values
        }
        #print(values)
        try:
            result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
                                                        valueInputOption=value_input_option, body=body).execute()
        except:
            print('Missed Row Output')
        else:
            ContactSheetOutput.currentRow += len(values)


        ContactSheetOutput.out_off('__error')
        return result
        
    @staticmethod
    def appendError(row, em):
        row.extend(['', '', '', '', '', '', 'Not Verified', em])
        return row















## Scrape Session Classes

class ScrapeSession(object):
    orgsForToday = ['National Association for Multi-Ethnicity In Communications (NAMIC)',
                    'Association for Women in Science',
                    'Brain Injury Association of America',
                    'American Society of Home Inspectors',
                    'NAADAC, the Association for Addiction Professionals',
                    'American Public Transportation Association',
                    'Indiana Soybean Alliance',
                    'Associated Builders and Contractors (ABC)',
                    'National Association of Social Workers',
                    'American Marketing Association (AMA)']

    errorCases = ['Arizona School Boards Association',
                  'Society of Petroleum Engineers',
                  'SSPC: the Society for Protective Coatings',
                  'American Association of Diabetes Educators']

    baseCase = ['National Association for Multi-Ethnicity In Communications (NAMIC)']
    
    appScraperQueue = None
    appCommandQueue = None

    def __init__(self, orgRecs):
        self.records = orgRecs
        ScrapeSession.set_orgs(self.records)
        self.startTime = None
        self.endTime = None
        self.numSitePings = 0
        self.runList = []
        
    def run_list(self, orgList):
        self.numSitePings = 0
        self.runList = orgList
        ContactScraperVerifier.clear_stats()
        
        ## ScrapeSession for APP:  Send Number of Orgs to be Scraped 'numOrgs'##
        ScrapeSession.push_to_app_queue({'numOrgs': len(self.runList)})

        try:
            self.startTime = dt.datetime.now()
            for org in self.runList:
                
                ## App for ScrapeSession: Listen For Stop or Pause Commands
                cmd = ScrapeSession.listen_for_cmd() 
                if cmd == 'stop':
                    print('HALTED SCRAPE SESSION')
                    self.endTime = dt.datetime.now()
                    self.get_early_termination_report()
                    return
                       
                ## ScrapeSession for APP:  Send scraping org to be Scraped 'scraping' ##
                ScrapeSession.push_to_app_queue({'scraping': org})
                
                vh = ContactCollector(org)
                self.numSitePings += 1
                ScrapeSession.push_to_app_queue({'complete': org})

        except Exception as e:
            print(e)
            self.endTime = dt.datetime.now()
            self.get_early_termination_report()
            
        else:
            self.endTime = dt.datetime.now()
            self.get_report()
        
    def run_orgs_for_today(self):
        self.run_list(ScrapeSession.orgsForToday)
        
    def run_all_orgs(self):
        self.run_list(ScrapeSession.orgs)
        
    def run_errors(self):
        self.run_list(ScrapeSession.errorCases)

    def run_base(self):
        self.run_list(ScrapeSession.baseCase)
        
    def get_report(self):
        noNothingPassed = len(ContactScraperVerifier.nothing_passed_merge)
        noNotExtracted = len(ContactScraperVerifier.not_extracted)
        noNotOpen = len(ContactScraperVerifier.link_not_open)
        noExtracted = len(ContactScraperVerifier.extracted)
        delta = self.endTime - self.startTime
        time = ScrapeSession.format_timedelta(delta)
        
        ## ScrapeSession for APP:  Send Report Here 'report' ##

        print('\n')
        print('--------------------------------------------------------------------------')
        print('Time of Scrape                                  \t\t  %s' % time)
        print('Number of Sites Attempted                       \t\t\t%s' % str(self.numSitePings))
        print('\n')
        print('Organizations with \nextracted contacts         \t\t\t\t\t\t%s\n' % str(noExtracted))
        #print('\n')
        print('Organizations without \nverified extractions    \t\t\t\t\t\t%s\n' % str(noNothingPassed))
        #print('\n')
        print('Organizations not \nextacted                    \t\t\t\t\t\t%s\n' % str(noNotExtracted))
        #print('\n')
        print('Organizations with links \nthat did not open    \t\t\t\t\t\t\t%s'   % str(noNotOpen))
        
    def get_early_termination_report(self):
        print('                 *** SCRAPE TERMINATED EARLRY ***                         ')
        print('              Attempted %s of %s organization links' % (str(self.numSitePings), str(len(self.runList))))
        print('--------------------------------------------------------------------------')
        self.get_report()
        
        
    @classmethod
    def set_orgs(cls,orgRecs):
        ScrapeSession.orgs = [orgRec['Organization'] for orgRec in orgRecs]
    
    ## Scraper Queue Methods
    @classmethod
    def set_app_scraper_queue(cls, queue):
        ScrapeSession.appScraperQueue = queue
    
    @classmethod
    def push_to_app_queue(cls, packet):
        ## Somtheing happens only if queue is set
        if ScrapeSession.appScraperQueue:
            ScrapeSession.appScraperQueue.put(packet)
    
    @classmethod
    def set_app_command_queue(cls, queue):
        ScrapeSession.appCommandQueue = queue
    
    @classmethod
    def push_to_command_queue(cls, packet):
        ## Somtheing happens only if queue is set
        if ScrapeSession.appCommandQueue:
            ScrapeSession.appCommandQueue.put(packet)
            
    @classmethod
    def listen_for_cmd(cls):
        if ScrapeSession.appCommandQueue:
            try:
                packet = ScrapeSession.appCommandQueue.get(0)
                if 'stop' in packet:
                    # The stop command has landed in scrap process
                    # resubmit the stop so that parent class on scraper thread gets it too
                    ScrapeSession.push_to_command_queue(packet)
                    return 'stop'
                if 'pause' in packet:
                    return 'pause'
                
                return None
                
            except queue.Empty:
                return None

            
    @staticmethod
    def format_timedelta(td):
        minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
        hours, minutes = divmod(minutes, 60)
        return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)


class ScrapeAll(ScrapeSession):
    def __init__(self, orgRecs):
        ScrapeSession.__init__(self, orgRecs)
        self.run_all_orgs()


class ScrapeForToday(ScrapeSession):
    def __init__(self, orgRecs):
        ScrapeSession.__init__(self, orgRecs) 
        self.run_orgs_for_today()


class ScrapeError(ScrapeSession):
    def __init__(self, orgRecs):
        ScrapeSession.__init__(self, orgRecs)
        self.run_errors() 


class ScrapeBase(ScrapeSession):
    def __init__(self, orgRecs):
        ScrapeSession.__init__(self, orgRecs)
        self.run_base()
















        
## Contact Checker Test Environment for Jupyter Notebook
## IMPORTANT: contactsScraper Must Be Run prior to running this here

if __name__ == '__main__':
#   print("Running Conact Checker Class Tests")
#   ContactSheetOutput.set_output(contactKeys)
#   VerificationHandler.set_orgRecords(dm.OrgSession(orgRecords))
    print('Local Contact Checker Ready')

