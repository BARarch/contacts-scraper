import sys
import time
from tkinter import *
import tkinter.ttk as ttk


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.parent = master
        self.pack()
        
        self.fmInitializationPanel = Frame().pack(expand=True, fill=BOTH, side=TOP)
        self.fmScraperControlPanel = Frame().pack(expand=True, fill=BOTH, side=TOP)
        self.fmSpreadSheetControlPanel = Frame().pack(expand=True, fill=BOTH, side=TOP)
        
        self.create_initialization_panel(self.fmInitializationPanel)
        self.create_scraper_control_panel(self.fmScraperControlPanel)
        self.create_spreadsheet_control_panel(self.fmSpreadSheetControlPanel)
        
    def create_initialization_panel(self, panel):
        self.initLabel = Label(panel, text='STARTUP STATUS')
        self.initLabel.pack()
    
    def create_scraper_control_panel(self, panel):
        self.scraperControlLabel = Label(panel, text='SCRAPER CONTROLS')
        self.scraperControlLabel.pack()
        
    def create_spreadsheet_control_panel(self, panel):
        self.spreadsheetControlLabel = Label(panel, text='SPEADSHEET CONTROLS')
        self.spreadsheetControlLabel.pack()



root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()