from Tkinter import *
import webbrowser
import os

class Reader(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		return

if __name__ == '__main__':
	root = Tk()
	root.title("xkcd Reader")
	root.geometry("200x200")

	reader = Reader(root)

	root.mainloop()