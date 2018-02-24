# Scraper-x-202101
Verifies and Updates contacts from a number of agency sites.

# Welcome to the GULP Scraper

## I.  Installation 

#### 1. Clone the repository into a readlity accessible folder using git clone
      
        $ git clone https://github.com/BARarch/Scraper-x-202101 [path to hosting folder]

#### 2. From the hosting folder Install packages for the Scaper using PIP
  
        $ pip install -r requirements_text.txt
        
#### 3. Verfify packages on system
  
        $ python packageTest.py
        
Here you should see that all of the packages tested are to pass.

![Package Test Report](/Doc-Material/Test.JPG)
        
#### 4. Run a test Scrape session
  
        $ python contactsScraperOpen.py
        
#### Special Note: Invalid Grant Error

After running this command, or any others in the project, you make get an long error trace that ends in an "Invalid Grant" message.  All this means is that google did not grant you access to the sheet and all the other googdies we use from them on the first try with the credentials they have on file.  This is fine, no big problem.  Just run the command again, complete the authentication step on the webpage that opens, and then you should be good to go!
        
when you see the 'SCRAPER OPEN' message and a chrome browser pop up on the desktop you are ready to run all scraper routines on your machine:

        $ python scrapeContacts.py
        
        $ python scrapeContactsBase.py
        
        $ python scrapeContactsError.py
        
        $ python scrapeContactsToday.py
  
  
  
## II.   Operation and Use

To scrape all organizations and update contacts navigate to the project folder and run

        $ python scrapeContacts.py

Gulp uses a browser emulator that scrapes each site.  From this browser all existing contacts are checked and new ones are found. Below is how the process should appear with the browser, command prompt and the Contacts google sheet.

![Desktop Overview](/Doc-Material/overview.jpg)

The program will process each organization by checking its contacts listed on the Contacts sheet.  You will see output for each orgnaization on the command prompts as this happens.

You will see each organization site render on the browser as the scraper checks it.  You may see the browers close and open again.  Don't worry this is normal.

As the scraper checks sites you will see the output from the scraper on the google sheet under the "Scraper Output" tab.  Status for contacts is displayed instintaniously on the sheet.

When the scraper completes the sesssion you will see a report showing information about all site scraped.  In testing during development the 421 site scrape usually takes around 1 hour and 15 minutes.  Times may vary depending on processor and connection speeds.

![Session Report](/Doc-Material/Complete.JPG)

## III.   Contacts and Scraper Sheets

Gulp is set to output all contacts from the scrape to the sheet under the "Scraper Output" tab.  Output includes verified contacts and non verified contacts on the "Contacts" tab in addition to newly discover contacts.  The Scraper Output sheet and the Contacts sheet have the same columns.  Gulp will allways read from the Contacts sheet and output to the Scraper Output sheet.  You will be transfering the output of the scraper by negotiating between the rows on the old Contacts sheet and the new Scraper Output sheet.  Allthough this process for refreshing the contacts is upto your choosing, an ideal routine is outlined below.  

#### 1.  Make a duplicate of the Scraper Output tab.

![Duplicate Scraper Output Sheet](/Doc-Material/duplicate.jpg)

#### 2.  Rename the "Contacts" tab to "Old Contacts" or some other name.

![Rename Contacts Sheet](/Doc-Material/rename.jpg)

#### 3.  Rename the "Copy of Scraper Output" tab to "Contacts"

#### 4.  Clear all rows in the Scraper Output tab so the system is ready for the next scraper run

![Clear Scraper Output](/Doc-Material/clear.jpg)


# The Samples Tab

![The Samples Tab](/Doc-Material/Samples.JPG)

This tab is were records are output from test case routines.  Running any of the following commands will output to the samples tab and not Scraper Output.  These test routines scrape no more than 10 sites each and complete in minutes.

        $ python scrapeContactsBase.py
        
        $ python scrapeContactsError.py
        
        $ python scrapeContactsToday.py        
        
        
