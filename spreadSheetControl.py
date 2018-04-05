import sys
import time
from tkinter import *
import tkinter.ttk as ttk

from ledRow import *

class SpreadSheetControl:

    RestoreText = 'This restores all original contacts from the Backup Sheet.  If there are new contacts from the scraper they will be lost'
    Paragraph = 'Welcome to the Gulp scraper.  I hope you are having a great day, and if not I hope I will make it better.'
    
    def __init__(self, master=None, handler=None):
        self.frame = ttk.Notebook(master)
        self.parent = master
        self.handler = handler
        self.frame.pack(side=TOP, expand=True, fill=X)

        self.transferTab = Frame(self.frame)
        self.restoreTab = Frame(self.frame)
        
        self.TRANSFER = Button(self.transferTab, width=12)
        self.TRANSFER.configure(command=self.handler.handle_transfer,
                               text='Transfer Scraped Contacts',
                               wraplength=50,
                               state='disabled')
        self.TRANSFER.pack(side=LEFT, anchor=W, expand=True, fill=Y)
        self.transferStatusFrame = ttk.Labelframe(self.transferTab, text='Transfer Status')
        self.transferStatusFrame.pack(side=RIGHT, expand=True, fill=Y)
        self.transferStatus = LEDRowDiscription(self.transferStatusFrame).bad().change_discription(SpreadSheetControl.Paragraph).good().blink()

        Label(self.restoreTab, text=SpreadSheetControl.RestoreText, wraplength=200, justify=LEFT, anchor=W).pack(side=LEFT, anchor=W)
        self.RESTORE = Button(self.restoreTab, width=12)
        self.RESTORE.configure(command=self.handler.handle_restore,
                               text='RESTORE CONTACTS',
                               wraplength=70,
                               state='disabled')
        self.RESTORE.pack(side=RIGHT, anchor=E, expand=True, fill=Y)

        self.frame.add(self.transferTab, text='Transfer', compound=TOP)
        self.frame.add(self.restoreTab, text='Restore Backup')

    def enable_transfer(self):
        pass

    def disable_transfer(self):
        pass

    def enable_restore(self):
        pass

    def disable_restore(self):
        pass

    def update_transfer_status(self, rowCounts):
        pass






if __name__ == '__main__':

    class TestSpreadSheetControl(Frame):
        def __init__(self, master=None):
            Frame.__init__(self)
            self.pack()

            self.manager = SpreadSheetControl(self, self)

        def handle_transfer(self):
            print('TRANSFER got pressed')

        def handle_restore(self):
            pring('RESTORE got pressed')

    root = Tk()
    app = TestSpreadSheetControl(master=root)
    app.mainloop()
    root.destroy()
