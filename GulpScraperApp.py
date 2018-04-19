import sys
import time
from tkinter import *
import tkinter.ttk as ttk
import queue
import threading
from datetime import datetime
from mainAppControl import *

if __name__ == '__main__':

    print('\t\t This is the GULP SCRAPER APP')
    print('\t\t   do not close this window')

    sys.stdout = open('output.txt', 'w')
    print ('Scraper started on ' + datetime.now().strftime('%a, %d %b %Y %H:%M:%S'))
    print()
          
    root = Tk()
    root.title("Gulp Scraper")
    img = PhotoImage(file='iconGulpPng.png')
    root.tk.call('wm', 'iconphoto', root._w, img)
    
    app = MainApplicationGD(master=root)
    app.after(500, app.startup)
    app.mainloop()
    root.destroy()