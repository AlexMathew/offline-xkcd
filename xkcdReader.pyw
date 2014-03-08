from Tkinter import *
import urllib
import webbrowser
import os
import sqlite3
from xkcd import xkcd

class Reader(Frame):
	def __init__(self, master, read=None):
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

		if not "Comics" in os.listdir("."):
			self.setup_page()		
		else:
			conn = sqlite3.connect("Comics/xkcd.db")
			c = conn.cursor()
			c.execute("SELECT * FROM xkcd")
			self.comics = c.fetchall()
			self.updated = max(self.comics)[0]
			c.close()
			conn.close()
			
			if not read:
				self.create_widgets()
		
		self.grid()

	def create_widgets(self):
		self.spacer1 = Label(self,
							text = "\n")
		self.spacer1.grid(row = 0, column = 0, columnspan = 4, sticky = W)

		self.intro = Label(self,
						   text = "\tTHE xkcd READER")
		self.intro.grid(row = 2, column = 0, columnspan = 4, sticky = W)

		self.spacer2 = Label(self,
							text = "\n")
		self.spacer2.grid(row = 3, column = 0, columnspan = 4, sticky = W)

		self.read = Button(self, 
							text = "READ !" , 
							command = self.read_page)
		self.read.grid(row = 5, column = 1, columnspan = 4, sticky = W)

		self.update = Button(self, 
							text = "UPDATE !" , 
							command = self.update_page)
		self.update.grid(row = 5, column = 3, columnspan = 4, sticky = W)
	
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
							text = "\n")
		self.spacer.grid(row = 7, column = 0, columnspan = 4, sticky = W)
				
		self.status = Text(self, 
						   width = 40, 
						   height = 10, 
						   wrap = WORD)
		self.status.delete(0.0, END)
		self.status.insert(0.0, "Click 'SET UP' to start loading the comics.. \n\n" + \
								"If a 'Not Responding' error appears, just ignore it. We're fine. ")
		self.status.grid(row = 9, column = 0, columnspan = 4, sticky = W)

		return

	def setup_db(self):
		try:
			os.mkdir("Comics")
			x = xkcd()
			conn = sqlite3.connect("Comics/xkcd.db")
			c = conn.cursor()
			c.execute("CREATE TABLE xkcd (num integer, title text, description text, explain text)")
			conn.commit()

			self.updated = int(x.comic_set[0][0])

			for comic in x.comic_set:
				number = int(comic[0])
				img, title, desc, explain = x.get_comic(number)
				c.execute("INSERT INTO xkcd VALUES (?,?,?,?)", (number, title, desc, explain))
				urllib.urlretrieve(img, "Comics/" + comic[0] + ".png")
				if number % 50 == 0:
					conn.commit()

			conn.commit()

			self.status.delete(0.0, END)
			self.status.insert(0.0, "And we're done ! Loaded till comic #" + str(self.updated))

			c.close()
			conn.close()

		except Exception as detail:
			self.status.delete(0.0, END)
			self.status.insert(0.0, detail)

		return

	def remove_home_widgets(self):
		self.spacer1.destroy()
		self.spacer2.destroy()
		self.intro.destroy()
		self.read.destroy()
		self.update.destroy()

		return

	def read_page(self):
		self.remove_home_widgets()
		self.quit()

		return

	def update_page(self):
		self.remove_home_widgets()

		self.intro = Label(self,
						   text = "Update your comic collection.\n\n")
		self.intro.grid(row = 2, column = 0, columnspan = 4, sticky = W)

		self.setup = Button(self, 
							text = "UPDATE !" , 
							command = self.update_db)
		self.setup.grid(row = 5, column = 2, columnspan = 4, sticky = W)
		
		self.spacer = Label(self,
							text = "\n")
		self.spacer.grid(row = 7, column = 0, columnspan = 4, sticky = W)
				
		self.status = Text(self, 
						   width = 40, 
						   height = 10, 
						   wrap = WORD)
		self.status.delete(0.0, END)
		self.status.insert(0.0, "Click 'UPDATE' to update your comic collection.. \n\n" + \
								"If a 'Not Responding' error appears, just ignore it. We're fine. ")
		self.status.grid(row = 9, column = 0, columnspan = 4, sticky = W)

		return	

	def update_db(self):
		try:
			x = xkcd()
			conn = sqlite3.connect("Comics/xkcd.db")
			c = conn.cursor()

			if not self.updated == int(x.comic_set[0][0]):
				for comic in x.comic_set:
					number = int(comic[0])
					if number == self.updated:
						break
					img, title, desc, explain = x.get_comic(number)
					c.execute("INSERT INTO xkcd VALUES (?,?,?,?)", (number, title, desc, explain))
					urllib.urlretrieve(img, "Comics/" + comic[0] + ".png")
					if number % 50 == 0:
						conn.commit()

				conn.commit()

				self.updated = int(x.comic_set[0][0]) 

				self.status.delete(0.0, END)
				self.status.insert(0.0, "And we're done ! Loaded till comic #" + str(self.updated))

			else:
				self.status.delete(0.0, END)
				self.status.insert(0.0, "We're already updated with the latest stuff.")

			c.close()
			conn.close()

		except Exception as detail:
			self.status.delete(0.0, END)
			self.status.insert(0.0, detail)

		return


if __name__ == '__main__':
	root = Tk()
	root.title("xkcd Reader")
	root.geometry("400x400+0+0")

	reader = Reader(root)

	root.mainloop()

	root.geometry("800x600+0+0")

	reader = Reader(root, 1)

	root.mainloop()