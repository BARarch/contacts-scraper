import sys
import time
from tkinter import *
import tkinter.ttk as ttk

ButtonWidth = 5

class ButtonPanel:
    def __init__(self, master=None, handler=None, buttonWidths=40, top=10, bottom=10):
        # Has a Frame
        self.frame = Frame(master)
        self.frame.pack(expand=True, fill=X, anchor=W)
        self.parent = master
        self.handler = handler
        
        self.handler.scrapeSelection.set('All') # set the default option
        self.dropDown = OptionMenu(self.frame, self.handler.scrapeSelection, 'All', 'Base', 'Today', 'Error')
        
        self.dropDown.pack(side=TOP, anchor=W, expand=YES, fill=X)
        self.disable_dropdown()
        
        self.bottom = Frame(self.frame)
        self.bottom.pack(side=TOP)
        self.QUIT = Button(self.bottom, width=7)
        self.QUIT.configure(command=self.handler.handle_quit,
                                text='QUIT',
                                fg='red')
        self.QUIT.pack(side=LEFT, padx=2)
        self.SCRAPE = Button(self.bottom, width=7)
        self.SCRAPE.configure(command=self.handler.handle_scrape,
                              text='Scrape',
                              fg='green',
                              state='disabled')
        self.SCRAPE.pack(side=LEFT, padx=2)
        
    def enable_scrape(self):
        self.SCRAPE.configure(state='active')
        return self
    
    def disable_scrape(self):
        self.SCRAPE.configure(state='disabled')
        return self
    
    def enable_quit(self):
        self.QUIT.configure(state='active')
        return self
    
    def disable_quit(self):
        self.QUIT.configure(state='disabled')
        return self
    
    def enable_dropdown(self):
        self.dropDown.configure(state='active')
        return self
    
    def disable_dropdown(self):
        self.dropDown.configure(state='disabled')
        return self

class ButtonPanelGD(ButtonPanel):
    def __init__(self, master=None, handler=None, buttonWidths=40, top=10, bottom=10):
        # Has a Frame
        self.frame = Frame(master) 
        self.parent = master
        self.handler = handler
        
        self.dropDown = OptionMenu(self.parent, self.handler.scrapeSelection, 'All', 'Base', 'Today', 'Error')
        self.handler.scrapeSelection.set('All') # set the default option
        self.dropDown.configure(width=8)
        self.dropDown.grid(row=0, column=0, columnspan=2, sticky=W+E, ipadx=2)
        #self.dropDown.pack(side=TOP, anchor=W, expand=YES, fill=X)
        self.disable_dropdown()
        
        
        self.QUIT = Button(self.parent, width=ButtonWidth)
        self.QUIT.configure(command=self.handler.handle_quit,
                                text='QUIT',
                                fg='red')
        self.QUIT.grid(row=1, column=0)
        #self.QUIT.pack(side=LEFT, padx=2)
        
        self.SCRAPE = Button(self.parent, width=ButtonWidth)
        self.SCRAPE.configure(command=self.handler.handle_scrape,
                              text='Scrape',
                              fg='green',
                              state='disabled')
        self.SCRAPE.grid(row=1, column=1)
        #self.SCRAPE.pack(side=LEFT, padx=2)
        
        #self.frame.grid()
        #self.frame.pack(expand=True, fill=X, anchor=W)
    
    
if __name__ == '__main__':
    
    class TestButtonPanel(Frame):
        def __init__(self, master=None):
            Frame.__init__(self)              # Do superclass init
            self.pack()
            self.scrapeSelection = StringVar(self)
            self.scrapeSelection.trace('w', self.change_dropdown)
            self.buttons = ButtonPanelGD(self, self)
            
        def do_somthing(self):
            pass
        
        def change_dropdown(self, *args):
            print(self.scrapeSelection.get())
            
        def handle_quit(self):
            self.buttons.enable_scrape().disable_quit().disable_dropdown()
        
        def handle_scrape(self):
            self.buttons.enable_quit().disable_scrape().enable_dropdown()
 

            
    root = Tk()
    root.title('The Button Panel')
    app = TestButtonPanel(master=root)
    app.mainloop()
    root.destroy()