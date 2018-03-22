from tkinter import *
import tkinter.ttk as ttk
from ledRow import *

if __name__ == '__main__':
    
    class TestInitPanel(Frame):
         def __init__(self, master=None):
            Frame.__init__(self)              # Do superclass init
            self.pack()
            self.left = Frame(self)
            self.left.pack(side=LEFT, anchor=N, expand=True)
            self.right = Frame(self)
            self.right.pack(side=RIGHT, anchor=N, expand=True)
            
            LEDRow(self.left, name="The Test Row", blink=1).active().message('hellothere').stop_blink().off().ready().blink().waiting()
            LEDRow(self.right, name="The Second Row", blink=1, blinkrate=2).waiting().stop_blink().active()
            LEDRow(self.right, name="The Third Row").ready().blink()
            
    root = Tk()
    root.title('LED Row')
    app = TestInitPanel(master=root)
    app.mainloop()
    root.destroy()