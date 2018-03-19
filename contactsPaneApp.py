import sys
import time
from tkinter import *
import tkinter.ttk as ttk
import testLeds as LED

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.parent = master
        self.pack()
        
        self.fmInitializationPanel = Frame(self).pack(expand=True, fill=BOTH, side=TOP)
        self.fmScraperControlPanel = Frame(self).pack(expand=True, fill=BOTH, side=TOP)
        self.fmSpreadSheetControlPanel = Frame(self).pack(expand=True, fill=BOTH, side=TOP)
        
        self.create_initialization_panel(self.fmInitializationPanel)
        self.create_scraper_control_panel(self.fmScraperControlPanel)
        self.create_spreadsheet_control_panel(self.fmSpreadSheetControlPanel)
        
    def create_initialization_panel(self, panel):
        self.initLabel = Label(panel, text='STARTUP STATUS')
        self.keyRecordsPane = ttk.Panedwindow(panel, orient=VERTICAL)
        self.fmKeysPanel = ttk.Labelframe(self.keyRecordsPane, text='KEYS')
        
        self.rowContactRecords = Frame(master=self.fmKeysPanel).pack(expand=True, fill=BOTH, side=TOP)
        self.crLabel = Label(self.rowContactRecords, text='Contact Records').pack()
        
        self.rowAjencyDirectory = Frame(master=self.fmKeysPanel).pack(expand=True, fill=BOTH, side=TOP)
        self.adLabel = Label(self.rowAjencyDirectory, text='Ajency Records').pack()
        
        self.fmRecordsPanel = ttk.Labelframe(self.keyRecordsPane, text ='RECORDS')
        
        
        self.keyRecordsPane.add(self.fmKeysPanel)
        self.keyRecordsPane.add(self.fmRecordsPanel)
        self.keyRecordsPane.pack(expand=True, fill=BOTH, side=LEFT)

        #self.initLabel.pack()



    
    def create_scraper_control_panel(self, panel):
        self.scraperControlLabel = Label(panel, text='SCRAPER CONTROLS')
        self.scraperControlLabel.pack()
        
    def create_spreadsheet_control_panel(self, panel):
        self.spreadsheetControlLabel = Label(panel, text='SPEADSHEET CONTROLS')
        self.spreadsheetControlLabel.pack()



root = Tk()
root.title('Contacts Pane')
app = Application(master=root)
app.mainloop()
root.destroy()