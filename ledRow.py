import sys
import time
from tkinter import *
import tkinter.ttk as ttk
from testLeds import *

StatusColor = '#BBBBBB'
LABELWIDTH = 20
STATUSWIDTH = 10
RowPadding = 5
Height = 2

class LEDRow:
    def __init__(self, master=None, name="NONE", blink=0, blinkrate=1):
        self.frame = Frame(master) 
        self.parent = master
        self.frame.pack(expand=True, side=TOP, anchor=W, fill=X)
        
        self.indicator = LED(master=self.frame, appearance=FLAT, shape=ROUND, blink=blink, blinkrate=blinkrate, bd=0, outline='grey')
        self.indicator.frame.pack(side=LEFT, anchor=W, expand=YES, padx=5, pady=1)
        self.name = Label(self.frame, text=name, anchor=W, width=LABELWIDTH)
        self.name.pack(side=LEFT, expand=YES, anchor=W,  fill=BOTH, pady=5)
        self.status = Label(self.frame, relief=SUNKEN, bg=StatusColor, fg="red", text='', width=STATUSWIDTH)
        self.status.pack(expand=True, fill=Y, side=RIGHT,anchor=E)
        
    def waiting(self):
        self.status.configure(fg="red", text='Waiting')
        self.indicator.blinkoff()
        self.indicator.alarm()
        return self
        
    def ready(self):
        self.status.configure(fg="green", text='Ready')
        self.indicator.blinkoff()
        self.indicator.turnon()
        return self
        
    def message(self, msg):
        self.status.configure(fg="Black", text=msg)
        self.status.update()
        return self

    def off(self):
        self.status.configure(text='')
        self.indicator.blinkoff()
        self.indicator.turnoff()
        return self
    
    def on(self, why=''):
        self.status.configure(fg="green", text=why)
        self.indicator.blinkoff()
        self.indicator.turnon()
        return self
        
    def active(self):
        self.indicator.blinkoff()
        self.indicator.warn()
        return self
        
    def blink(self):
        self.indicator.blinkon()
        return self
    
    def stop_blink(self):
        self.indicator.blinkoff()
        return self

class LEDRowGD(LEDRow):
    def __init__(self, master=None, name="NONE", blink=0, blinkrate=1):
        self.frame = Frame(master) 
        self.parent = master
        self.frame.grid()
        
        self.indicator = LED(master=self.frame, appearance=FLAT, shape=ROUND, blink=blink, blinkrate=blinkrate, bd=0, outline='grey')
        self.indicator.frame.grid(row=0)
        #self.indicator.frame.pack(side=LEFT, anchor=W, expand=YES, padx=5, pady=1)
        
        self.name = Label(self.frame, text=name, anchor=W, width=LABELWIDTH, height=Height)
        self.name.grid(row=0, column=1)
        #self.name.pack(side=LEFT, expand=YES, anchor=W,  fill=BOTH, pady=5)
        
        self.status = Label(self.frame, relief=SUNKEN, bg=StatusColor, fg="red", text='', width=STATUSWIDTH, height=Height)
        self.status.grid(row=0, column=2)
        #self.status.pack(expand=True, fill=Y, side=RIGHT,anchor=E)
    
    
class LEDRowNoMsg(LEDRow):
    def __init__(self, master=None, name="NONE", blink=0, blinkrate=1):
        LEDRow.__init__(self, master=master, name=name, blink=blink, blinkrate=blinkrate)
        self.frame.pack_forget()
        self.status.pack_forget()
        self.frame.pack(expand=True, side=TOP, anchor=W)
              
    def waiting(self):
        self.indicator.blinkoff()
        self.indicator.alarm()
        return self
        
    def ready(self):
        self.indicator.blinkoff()
        self.indicator.turnon()
        return self

    def off(self):
        self.indicator.blinkoff()
        self.indicator.turnoff()
        return self
        
    def message(self, msg):
        return self

class LEDRowNoMsgGD(LEDRowNoMsg):
    def __init__(self, master=None, name="NONE", blink=0, blinkrate=1):
        self.frame = Frame(master) 
        self.parent = master
        self.frame.grid(sticky=W)
        
        self.indicator = LED(master=self.frame, appearance=FLAT, shape=ROUND, blink=blink, blinkrate=blinkrate, bd=0, outline='grey')
        self.indicator.frame.grid(row=0)
        #self.indicator.frame.pack(side=LEFT, anchor=W, expand=YES, padx=5, pady=1)
        
        self.name = Label(self.frame, text=name, anchor=W, width=LABELWIDTH, height=Height)
        self.name.grid(row=0, column=1)
        #self.name.pack(side=LEFT, expand=YES, anchor=W,  fill=BOTH, pady=5)
        

class LEDRowDiscription(LEDRow):
    def __init__(self, master=None, name="NONE", blink=0, blinkrate=1):
        LEDRow.__init__(self, master=master, name=name, blink=blink, blinkrate=blinkrate)
        self.frame.pack_forget()
        self.status.pack_forget()
        self.frame.pack(expand=True, side=TOP, anchor=W)
        self.bottomFrame = Frame(master)
        self.bottomFrame.pack(expand=True, side=TOP, fill=X, anchor=W)
        self.discription = Label(self.bottomFrame, text='This is a lot of text I want it to wrap and wrap it will',
                                                   wraplength=200,
                                                   justify=LEFT,
                                                   anchor=W)

        self.discription.pack(anchor=W)

    def message(self, msg):
        self.name.configure(text=msg)
        return self

    def change_discription(self, msg):
        self.discription.configure(text=msg)
        return self

    def waiting(self):
        return self
        
    def ready(self):
        return self

    def active(self):
        return self

    def bad(self):
        self.indicator.blinkoff()
        self.indicator.alarm()
        return self
        
    def good(self):
        self.indicator.blinkoff()
        self.indicator.turnon()
        return self

    def off(self):
        self.indicator.blinkoff()
        self.indicator.turnoff()
        return self   



        #wraplength=LABELWIDTH, justify=LEFT,

class LEDRowDiscriptionGD(LEDRowDiscription):
    def __init__(self, master=None, name="NONE", blink=0, blinkrate=1):
        self.frame = Frame(master) 
        self.parent = master
        self.frame.grid(sticky=W)
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=1)
        
        self.indicator = LED(master=self.frame, appearance=FLAT, shape=ROUND, blink=blink, blinkrate=blinkrate, bd=0, outline='grey')
        self.indicator.frame.grid(row=0, column=0, sticky=W)
        
        #self.indicator.frame.pack(side=LEFT, anchor=W, expand=YES, padx=5, pady=1)
        
        self.name = Label(self.frame, text=name, anchor=W, width=LABELWIDTH, height=Height)
        self.name.grid(row=0, column=1, sticky=W)
        
        #self.name.pack(side=LEFT, expand=YES, anchor=W,  fill=BOTH, pady=5)

        self.discription = Label(self.frame, text='This is a lot of text I want it to wrap and wrap it will',
                                                   wraplength=200,
                                                   justify=LEFT,
                                                   anchor=W)
        self.discription.grid(row=2, column=0, columnspan=2)


        
        
if __name__ == '__main__':

    paragraph = 'Welcome to the Gulp scraper.  I hope you are having a great day, and if not I hope I will make it better.'
    
    class TestLEDRow(Frame):
         def __init__(self, master=None):
            Frame.__init__(self)              # Do superclass init
            self.pack()
            LEDRowGD(self, name="The Test Row", blink=1).active().message('hellothere').stop_blink().off().ready().blink().waiting()
            LEDRowGD(self, name="The Second Row", blink=1, blinkrate=2).waiting()
            LEDRowGD(self, name="The Third Row").ready().blink()
            LEDRowNoMsgGD(self, name="No Msg")
            LEDRowDiscriptionGD(self).bad().change_discription(paragraph).good().blink()
            LEDRowGD(self, name="After Name Change").ready().blink().waiting()
            
    root = Tk()
    root.title('LED Row')
    app = TestLEDRow(master=root)
    app.mainloop()
    root.destroy()