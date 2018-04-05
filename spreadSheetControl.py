import sys
import time
from tkinter import *
import tkinter.ttk as ttk

from ledRow import *

class SpreadSheetControl:

    RestoreText = 'This restores all original contacts from the Backup Sheet.  If there are new contacts from the scraper they will be lost'
    Paragraph = 'Welcome to the Gulp scraper.  Loading scraper output and contacts'
    
    def __init__(self, master=None, handler=None):
        self.frame = ttk.Notebook(master)
        self.parent = master
        self.handler = handler
        #self.frame.pack(side=TOP, expand=True, fill=X)
        self.frame.pack(side=TOP, expand=True, anchor=W, fill=X)

        self.transferTab = Frame(self.frame)
        self.restoreTab = Frame(self.frame)
        
        self.TRANSFER = Button(self.transferTab, width=12)
        self.TRANSFER.configure(command=self.handler.handle_transfer,
                               text='Transfer Scraped Contacts',
                               wraplength=50,
                               state='disabled')
        self.TRANSFER.pack(side=LEFT, anchor=W, expand=True, fill=Y)
        self.transferStatusFrame = ttk.Labelframe(self.transferTab, text='Transfer Status')
        self.transferStatusFrame.pack(side=LEFT, expand=True, fill=X, anchor=W)
        self.transferStatus = LEDRowDiscription(self.transferStatusFrame, name='Checking Transfer Status...').bad().change_discription(SpreadSheetControl.Paragraph).good().blink()

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
        self.TRANSFER.configure(state='active')
        return self

    def disable_transfer(self):
        self.TRANSFER.configure(state='disabled')
        return self

    def enable_restore(self):
        self.RESTORE.configure(state='active')
        return self

    def disable_restore(self):
        self.RESTORE.configure(state='disabled')
        return self

    def update_transfer_status(self, rowCounts=None):
        if rowCounts:
            contacts = rowCounts['contact counts']
            outputs = rowCounts['output counts']

            if contacts > outputs:
                self.disable_transfer()
                self.transferStatus.message('Not Ready')
                self.transferStatus.bad()
                discription = 'There are only {} contacts in the scraper output and {} in contacts.'.format(str(outputs), str(contacts))
                self.transferStatus.change_discription(discription)
            else:
                self.enable_transfer()
                self.transferStatus.message('Good')
                self.transferStatus.good()
                discription = 'It is okay to transfer the scraper output to the contacts.'
                self.transferStatus.change_discription(discription)
        else:
            self.disable_transfer()
            self.transferStatus.message('Updating Contacts')
            self.transferStatus.good().blink()
            discription = 'We will know if transfers are possible when the scrape is complete.'
            self.transferStatus.change_discription(discription)

        return self







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
