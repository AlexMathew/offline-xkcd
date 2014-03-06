from Tkinter import *
import urllib
import webbrowser
import os
import sqlite3
from xkcd import xkcd

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
		else:
			self.create_widgets()
		
		self.grid()

	def create_widgets(self):
		return

	def setup_page(self):
		self.intro = Label(self,
						   text = "Looks like this is the first time you are running this here. \n\n" + \
						   		  "Let's set up your collection. \n\n Don't stop the program or switch off your internet " + \
						   		  "in the middle. \n\n\n")
		self.intro.grid(row = 2, column = 0, columnspan = 4, sticky = W)

		self.setup = Button(self, 
							text = "SET UP !" , 
							command = self.setup_db)
		self.setup.grid(row = 5, column = 2, columnspan = 4, sticky = W)
		
		self.spacer = Label(self,
							text = "\n\n")
		self.spacer.grid(row = 7, column = 0, columnspan = 4, sticky = W)
		
		return

	def setup_db(self):
		os.mkdir("Comics")
		x = xkcd()
		conn = sqlite3.connect("xkcd.db")
		c = conn.cursor()
		
		self.status = Text(self, 
						   width = 90, 
						   height = 10, 
						   wrap = WORD)
		self.status.delete(0.0, END)
		self.status.insert(0.0, "")
		self.status.grid(row = 9, column = 0, columnspan = 4, sticky = W)

		for comic in x.comic_set:
			number = int(comic[0])
			img, title, desc, explain = x.get_comic(number)
			c.execute("INSERT INTO xkcd VALUES (?,?,?,?)", (number, title, desc, explain))
			urllib.urlretrieve(img, "Comics/" + comic[0] + ".png")
			self.status.delete(0.0, END)
			self.status.insert(0.0, "Updating #" + comic[0] + " - " + title)
			if number % 50 == 0:
				conn.commit()

		conn.commit()

		return

if __name__ == '__main__':
	root = Tk()
	root.title("xkcd Reader")
	root.geometry("800x600")

	reader = Reader(root)

	root.mainloop()