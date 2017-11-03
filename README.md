# Scraper-x-202101
Verifies and Updates contacts from a number of agency sites.

# Welcome to the GULP Scraper

## I.  Installation 



1. Clone the repository into a readlity accessible folder using git clone
      
        $ git clone https://github.com/BARarch/Scraper-x-202101 [path to hosting folder]

2. From the hosting folder Install packages for the Scaper using PIP
  
        $ pip install -r requirements_text.txt
        
3. Verfify packages on system
  
        $ python packageTest.py
        
4. Run a test Scrape session
  
        $ python contactsScraperOpen.py
        
when you see the 'SCRAPER OPEN' message you are ready to run all scraper routines on your machine:

        $ python scrapeContacts.py
        
        $ python scrapeContactsBase.py
        
        $ python scrapeContactsError.py
        
        $ python scrapeContactsToday.py
  
  
  
## II.   Opperation and Use

        $ python scrapeContacts.py

The scraper uses a browser emulator that scrapes each site.  From this browser all existing contacts are checked and new ones are found. Below is how the process should appear with the browser, command prompt and the Contacts google sheet.

![alt text](/Doc-Material/overview.JPG)

The program will process each organization by checking its contacts listed on the Contacts sheet.  You will see output for each orgnaization on the command prompts as this happens.

You will see each organization site render on the browser as the scraper checks it.  You may see the browers close and open again.  Don't worry this is normal.

As the scraper checks sites you will see the output from the scraper on the google sheet under the "Scraper Output" tab.  Status for contacts is displayed instintaniously on the sheet.

When the scraper completes the sesssion you will see a report showing information about all site scraped.  In testing during development the 421 site scrape usually takes around 1 hour and 15 minutes.  Times may vary depending on processor and connection speeds.

![alt text](/Doc-Material/complete.JPG)

## III.   Contacts and Scraper Sheets

  
        
        
        
