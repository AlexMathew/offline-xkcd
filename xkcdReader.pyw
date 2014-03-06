from Tkinter import *
import webbrowser
import os
import sqlite3

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

		conn = sqlite3.connect("xkcd.db")
		c = conn.cursor()
		c.execute("SELECT * FROM xkcd")
		comics = c.fetchall()
		c.close()
		conn.close()

		if not len(comics):
			self.setup_page()		
		
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		return

	def setup_page(self):
		return


if __name__ == '__main__':
	root = Tk()
	root.title("xkcd Reader")
	root.geometry("800x600")

	reader = Reader(root)

	root.mainloop()