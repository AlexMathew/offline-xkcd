from Tkinter import *
import webbrowser
import os

class Reader(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)

		self.menubar = Menu(self)

		menu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="Options", menu=menu)
		menu.add_command(label="Reader")
		menu.add_command(label="Update comic collection")

		menu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="Help", menu=menu)
		menu.add_command(label="Docs")
		menu.add_command(label="About")
		menu.add_command(label="Credits")

		self.master.config(menu=self.menubar)
		
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