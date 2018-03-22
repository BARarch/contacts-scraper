from tkinter import *
import tkinter.ttk as ttk
from ledRow import *

class InitPanel:
    def __init__(self, master=None):
        self.frame = Frame(master)
        self.parent = master
        self.frame.pack(expand=True, side=TOP, anchor=N)
        self.left = Frame(self.frame)
        self.left.pack(side=LEFT, anchor=N, expand=True)
        self.right = Frame(self.frame)
        self.right.pack(side=RIGHT, anchor=N, expand=True, pady=17)

        self.p = ttk.Panedwindow(self.left, orient=VERTICAL)
        # first pane, which would get widgets gridded into it:
        self.keysFrame = ttk.Labelframe(self.left, text='KEYS')
        self.keysFrame.pack(side=TOP, anchor=W, expand=True)
        self.recordsFrame = ttk.Labelframe(self.left, text='RECORDS')
        self.recordsFrame.pack(side=TOP, anchor=W, expand=True)# second pane
        #self.p.add(self.keysFrame)
        #self.p.add(self.recordsFrame)
        
        self._contactKeys = LEDRow(self.keysFrame, name="Contact Keys").off()
        self._directoryKeys = LEDRow(self.keysFrame, name="Directory Keys").off()   
        self._contactRecords = LEDRow(self.recordsFrame, name="Contact Records").off()
        self._agencyDirectory = LEDRow(self.recordsFrame, name="Agency Directory").off()
        
        #self._contactKeys = LEDRow(self.left, name="Contact Keys").off()
        #self._directoryKeys = LEDRow(self.left, name="Directory Keys").off()   
        #self._contactRecords = LEDRow(self.left, name="Contact Records").off()
        #self._agencyDirectory = LEDRow(self.left, name="Agency Directory").off()
        
        
        self._data = LEDRow(self.right, name="Data").off()
        self._output = LEDRow(self.right, name="Output").off()
        self._browserDriver = LEDRowNoMsg(self.right, name="Browser/Driver").off()
        self._contactChecker = LEDRow(self.right, name="Contact Checker").off().active().blink()
        
    ## Startup Phases from Off
    def contact_keys_waiting():
        pass
    def contact_keys_ready():
        pass
    
    def directory_keys_waiting():
        pass
    def directory_keys_ready():
        pass
    
    def contact_records_waiting():
        pass
    def contact_records_ready():
        pass
    
    def agency_directory_waiting():
        pass
    def agency_directory_ready():
        pass
    
    def data_waiting():
        pass
    def data_ready():
        pass
    
    def output_waiting():
        pass
    def output_ready():
        pass
    
    def browser_driver_waiting():
        pass
    def browser_driver_ready():
        pass
    
    def scraper_waiting():
        pass
      
    # Contact Scraper Open
    def scraper_open_phase():
        pass
    
    # Contact Scraper Running
    def scraper_running_phase():
        pass
    
    # Contact Scrape Feedback Methods for Init Panel
    def request_on():
        pass
    def request_off():
        pass
    
    def output_on():
        pass
    def output_off():
        pass
    
    def agency_report_on():
        pass
    def agency_report_off():
        pass

if __name__ == '__main__':
    ## Get Scraper Thread
    ## Get initalization queue
    ## ...and Test Startup
    
    
    class TestInitPanel(Frame):
         def __init__(self, master=None):
            Frame.__init__(self, master)              # Do superclass init
            self.pack()
            InitPanel(self)
            
    root = Tk()
    root.title('Initialization Panel Test')
    app = TestInitPanel(master=root)
    app.mainloop()
    root.destroy()