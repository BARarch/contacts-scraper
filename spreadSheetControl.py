import sys
import time
from tkinter import *
import tkinter.ttk as ttk

from ledRow import *

class SpreadSheetControl:
	def __init__(self, master=None, handler=None):
		self.frame = Frame(master)
		self.frame = master
		self.buttonHandler = handler
		self.frame.pack(side=TOP)




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
