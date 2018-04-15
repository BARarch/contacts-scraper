from tkinter import *
import tkinter.ttk as ttk
from ledRow import *
import time

FramePanelHorizontalPadding = 13
FramePanelTopPadding = 5
FramePanelBottomPadding = 5
FramePanelVerticalSeparation = 18
IndicatorsLeftSidePadding = 13
IndicatorsRightSidePadding = 21

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
        self.keysFrame = ttk.Labelframe(self.left, text='KEYS')
        self.keysFrame.pack(side=TOP, anchor=W, expand=True)
        self.recordsFrame = ttk.Labelframe(self.left, text='RECORDS')
        self.recordsFrame.pack(side=TOP, anchor=W, expand=True)# second panes
        
        self._contactKeys = LEDRow(self.keysFrame, name="Contact Keys").off()
        self._directoryKeys = LEDRow(self.keysFrame, name="Directory Keys").off()   
        self._contactRecords = LEDRow(self.recordsFrame, name="Contact Records").off()
        self._agencyDirectory = LEDRow(self.recordsFrame, name="Agency Directory").off()
                    
        self._data = LEDRow(self.right, name="Data").off()
        self._output = LEDRow(self.right, name="Output").off()
        self._browserDriver = LEDRowNoMsg(self.right, name="Browser/Driver").off()
        self._contactChecker = LEDRow(self.right, name="Contact Checker").off().active().blink()
        
    ## Startup Phases from Off
    def contact_keys_waiting(self):
        self._contactKeys.waiting()
        
    def contact_keys_ready(self):
        self._contactKeys.ready()
    
    def directory_keys_waiting(self):
        self._directoryKeys.waiting()
        
    def directory_keys_ready(self):
        self._directoryKeys.ready()
    
    def contact_records_waiting(self):
        self._contactRecords.waiting()
    def contact_records_ready(self):
        self._contactRecords.ready()
    
    def agency_directory_waiting(self):
        self._agencyDirectory.waiting()
    def agency_directory_ready(self):
        self._agencyDirectory.ready()
    
    def data_waiting(self):
        self._data.waiting()
    def data_ready(self):
        self._data.ready()
    
    def output_waiting(self):
        self._output.waiting()
    def output_ready(self):
        self._output.ready()
    
    def browser_driver_waiting(self):
        self._browserDriver.waiting()
    def browser_driver_ready(self):
        self._browserDriver.ready()
    
    def scraper_waiting(self):
        self._contactChecker.message('Waiting')
      
    # Contact Scraper Open
    def scraper_open_phase(self):
        #self._contactChecker.message('Ready').indicator.alarm()
        self._contactRecords.off().message("")
        self._agencyDirectory.off().message("")
        self._data.off().message("")
        self._output.off().message("")
        self._browserDriver.off()
        
    
    # Contact Scrape Feedback Methods for Init Panel
    def request_on(self):
        self._browserDriver.active()
    def request_off(self):
        self._browserDriver.off()
    
    def output_on(self):
        self._output.active()
    def output_off(self):
        self._output.off()
    
    def agency_report_on(self):
        self._agencyDirectory.active()
    def agency_report_off(self):
        self._agencyDirectory.off()

class InitPanelGD(InitPanel):
    def __init__(self, master=None):
        self.frame = Frame(master)
        self.parent = master
        

        self.left = Frame(self.frame)
        self.left.grid(sticky=N+W, padx=IndicatorsLeftSidePadding)
        #self.left.pack(side=LEFT, anchor=N, expand=True)

        self.right = Frame(self.frame)
        self.right.grid(row=0, column=1, sticky=E+N, padx=IndicatorsRightSidePadding)
        #self.right.pack(side=RIGHT, anchor=N, expand=True, pady=17)

        self.keysFrame = ttk.Labelframe(self.left, text='KEYS', padding=(FramePanelHorizontalPadding ,FramePanelTopPadding, FramePanelHorizontalPadding, FramePanelBottomPadding))
        self.recordsFrame = ttk.Labelframe(self.left, text='RECORDS', padding=(FramePanelHorizontalPadding ,FramePanelTopPadding, FramePanelHorizontalPadding, FramePanelBottomPadding))
        
        self._contactKeys = LEDRowGD(self.keysFrame, name="Contact Keys").off()
        self._directoryKeys = LEDRowGD(self.keysFrame, name="Directory Keys").off()   
        self._contactRecords = LEDRowGD(self.recordsFrame, name="Contact Records").off()
        self._agencyDirectory = LEDRowGD(self.recordsFrame, name="Agency Directory").off()
        
        LEDRowBlankGD(self.right, topPad=1)            
        self._data = LEDRowGD(self.right, name="Data", topPad=50).off()
        self._output = LEDRowGD(self.right, name="Output").off()
        self._browserDriver = LEDRowNoMsgGD(self.right, name="Browser/Driver").off()
        self._contactChecker = LEDRowGD(self.right, name="Contact Checker").off().active().blink()


        self.keysFrame.grid()
        
        #self.keysFrame.pack(side=TOP, anchor=W, expand=True)

        self.recordsFrame.grid(row=1)
        #self.recordsFrame.pack(side=TOP, anchor=W, expand=True)# second panes
        
        self.frame.grid(sticky=E+W)
        self.left.rowconfigure(1, pad=FramePanelVerticalSeparation)
        #self.frame.pack(expand=True, side=TOP, anchor=N)
        self.frame.columnconfigure(0, weight=1)
        #self.left.columnconfigure(0, ipad=IndicatorsLeftSidePadding)
        self.frame.columnconfigure(1, weight=0)
        #self.right.columnconfigure(0, ipad=IndicatorsRightSidePadding)
        
        

if __name__ == '__main__':
    ## Get Scraper Thread
    ## Get initalization queue
    ## ...and Test Startup
    
    
    class TestInitPanel(Frame):
        def __init__(self, master=None):
            Frame.__init__(self, master)              # Do superclass init
            self.pack()
            self.ip = InitPanelGD(self)
            
        def contact_keys_waiting_test(self):
            self.ip.contact_keys_waiting()
            time.sleep(2)
            self.after(200, self.directory_keys_waiting_test())
            
        def directory_keys_waiting_test(self):
            self.ip.contact_keys_ready()
            self.ip.directory_keys_waiting()
            time.sleep(2)
            self.after(200, self.contact_records_waiting_test())
            
        def contact_records_waiting_test(self):
            self.ip.directory_keys_ready()
            self.ip.contact_records_waiting()
            time.sleep(2)
            self.after(200, self.agency_directory_waiting_test()) 
            
        def agency_directory_waiting_test(self):
            self.ip.contact_records_ready()
            self.ip.agency_directory_waiting()
            time.sleep(2)
            self.after(200, self.data_waiting_test())
            
        def data_waiting_test(self):
            self.ip.agency_directory_ready()
            self.ip.data_waiting()
            time.sleep(2)
            self.after(200, self.output_waiting_test())
            
        def output_waiting_test(self):
            self.ip.data_ready()
            self.ip.output_waiting()
            time.sleep(2)
            self.after(200, self.browser_driver_waiting_test())
            
        def browser_driver_waiting_test(self):
            self.ip.output_ready()
            self.ip.browser_driver_waiting()
            time.sleep(2)
            self.after(200, self.scraper_waiting_test()) 
            
        def scraper_waiting_test(self):
            self.ip.browser_driver_ready()
            self.ip.scraper_waiting()
            time.sleep(2)
            self.after(200, self.scraper_open_phase_test())
            
        def scraper_open_phase_test(self):
            self.ip.scraper_open_phase()
            time.sleep(.5)
            self.after(200, self.scraper_running_phase_test())
            
        def scraper_running_phase_test(self):
            #self.ip.scraper_running_phase()
            time.sleep(.5)
            self.after(200, self.request_test())
            
        def request_test(self):
            self.ip.request_on()
            time.sleep(.2)
            self.ip.request_off()
            self.after(200, self.output_test())
            
        def output_test(self):
            self.ip.output_on()
            time.sleep(.2)
            self.ip.output_off()
            self.after(200, self.agency_report_test())
            
        def agency_report_test(self):
            self.ip.agency_report_on()
            time.sleep(.2)
            self.ip.agency_report_off()
            self.after(200, self.scraper_running_phase_test())
            
    root = Tk()
    root.title('Initialization Panel Test')
    app = TestInitPanel(master=root)
    #app.after(200, app.contact_keys_waiting_test())
    app.mainloop()
    root.destroy()