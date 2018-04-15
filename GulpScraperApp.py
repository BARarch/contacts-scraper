import sys
import time
from tkinter import *
import tkinter.ttk as ttk
import queue
import threading

from mainAppControl import *

if __name__ == '__main__':
          
    root = Tk()
    app = MainApplicationGD(master=root)
    app.after(500, app.startup)
    app.mainloop()
    root.destroy()