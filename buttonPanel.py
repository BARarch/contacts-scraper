import sys
import time
from tkinter import *
import tkinter.ttk as ttk

class ButtonPanel:
    def __init__(self, master=None, handler=None, buttonWidths=40, top=10, bottom=10):
        # Has a Frame
        self.frame = Frame(master)
        self.frame.pack()
        self.parent = master
        self.handler = handler
        
        self.dropDown = OptionMenu(self.frame, self.handler.scrapeSelection, 'All', 'Base', 'Today', 'Error')
        self.handler.scrapeSelection.set('Today') # set the default option
        self.dropDown.pack(side=TOP)
        
        self.bottom = Frame(self.frame)
        self.bottom.pack(side=TOP)
        self.QUIT = Button(self.bottom)
        self.QUIT.configure(command=self.handler.handle_quit,
                                text='QUIT',
                                fg='red')
        self.QUIT.pack(side=LEFT)
        self.SCRAPE = Button(self.bottom)
        self.SCRAPE.configure(command=self.handler.handle_scrape,
                              text='Scrape',
                              fg='green',
                              state='disabled')
        self.SCRAPE.pack(side=LEFT)
        
    
    
if __name__ == '__main__':
    
    class TestButtonPanel(Frame):
        def __init__(self, master=None):
            Frame.__init__(self)              # Do superclass init
            self.pack()
            self.scrapeSelection = StringVar(self)
            self.scrapeSelection.trace('w', self.change_dropdown)
            self.buttons = ButtonPanel(self, self)
            
        def do_somthing(self):
            pass
        
        def change_dropdown(self, *args):
            print(self.scrapeSelection.get())
            
        def handle_quit(self):
            pass
        
        def handle_scrape(self):
            pass
 

            
    root = Tk()
    root.title('The Button Panel')
    app = TestButtonPanel(master=root)
    app.mainloop()
    root.destroy()