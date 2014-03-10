from Tkinter import *
import urllib
import webbrowser
import os
import sqlite3
import random
import tkMessageBox
from PIL import ImageTk, Image
from xkcd import xkcd

if not "Comics" in os.listdir("."):
	current_op = 3		
else:
	current_op = 0

class Reader(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)

		self.menubar = Menu(self)

		readmenu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="Reader Options", menu=readmenu)
		readmenu.add_command(label="Reader", command=self.read_page_setter)
		readmenu.add_command(label="Update comic collection", command=self.update_page_setter)
		readmenu.add_separator()		
		readmenu.add_command(label="Exit", command=self.quit)

		helpmenu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="Help", menu=helpmenu)
		helpmenu.add_command(label="Check out xkcd", command=self.open_xkcd)
		helpmenu.add_command(label="About", command=self.about_msg)
		helpmenu.add_command(label="Credits")

		self.master.config(menu=self.menubar)

		self.updated = 0
		self.current_widgets = []

		global current_op

		if not "Comics" in os.listdir("."):
			self.setup_page()		
		else:
			if current_op == 0:
				self.create_widgets()
			elif current_op == 1:
				conn = sqlite3.connect("Comics/xkcd.db")
				c = conn.cursor()
				c.execute("SELECT * FROM xkcd")
				self.comics = c.fetchall()
				self.updated = max(self.comics)[0]
				self.current_comic = self.updated  
				c.close()
				conn.close()
				self.read_page()
			elif current_op == 2:
				self.update_page()
			else:
				pass
		
		current_op = -1

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
							command = self.read_page_setter)
		self.read.grid(row = 5, column = 1, columnspan = 4, sticky = W)

		self.update = Button(self, 
							text = "UPDATE !" , 
							command = self.update_page_setter)
		self.update.grid(row = 5, column = 3, columnspan = 4, sticky = W)
	
		self.current_widgets.extend([self.spacer1, self.intro, self.spacer2, self.read, self.update])

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
		self.status.insert(0.0, "Click 'SET UP' to start loading the comics.. \n" + \
								"This may take a very long time to run. So just run it, and carry on with your work for an " + \
								"hour or so. Trust me, it's worth the wait !\n" + \
								"If a 'Not Responding' error appears, just ignore it. We're fine. ")
		self.status.grid(row = 9, column = 0, columnspan = 4, sticky = W)

		self.current_widgets.extend([self.intro, self.setup, self.spacer, self.status])

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

			for comic in reversed(x.comic_set):
				number = int(comic[0])
				img, title, desc, explain = x.get_comic(number)
				c.execute("INSERT INTO xkcd VALUES (?,?,?,?)", (number, title, desc, explain))
				urllib.urlretrieve(img, "Comics/" + comic[0] + ".png")
				if number % 10 == 0:
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

	def remove_widgets(self):
		for widget in self.current_widgets:
			widget.destroy()
		self.current_widgets = []

		return

	def read_page_setter(self):
		self.remove_widgets()

		global current_op
		current_op = 1
		self.quit()

		return

	def read_page(self):
		img = ImageTk.PhotoImage(Image.open("Comics/" + str(self.updated) +".png"))
		self.panel = Label(self, image = img)
		self.panel.image = img
		self.panel.grid(row = 2, column = 0, columnspan = 4, sticky = W)

		return

	def update_page_setter(self):
		self.remove_widgets()

		global current_op
		current_op = 2
		self.quit()

		return

	def update_page(self):	
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

		self.current_widgets.extend([self.intro, self.setup, self.spacer, self.status])

		return	

	def update_db(self):
		try:
			x = xkcd()
			conn = sqlite3.connect("Comics/xkcd.db")
			c = conn.cursor()
			c.execute("SELECT * FROM xkcd")
			self.comics = c.fetchall()
			self.updated = max(self.comics)[0]

			if not self.updated == int(x.comic_set[0][0]):
				for comic in reversed(x.comic_set[:-self.updated]):
					number = int(comic[0])
					img, title, desc, explain = x.get_comic(number)
					c.execute("INSERT INTO xkcd VALUES (?,?,?,?)", (number, title, desc, explain))
					urllib.urlretrieve(img, "Comics/" + comic[0] + ".png")
					if number % 10 == 0:
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

	def about_msg(self):
		tkMessageBox.showinfo("About", "xkcd Reader is an offline reader for xkcd webcomics.\n\nVersion 1.0")
		return

	def open_xkcd(self):
		webbrowser.open_new_tab("http://xkcd.com")
		return

if __name__ == '__main__':
	global current_op

	while(True):
		root = Tk()
		root.title("xkcd Reader")

		if current_op == -1:
			break
		elif current_op == 0:
			root.geometry("200x200+0+0")
		elif current_op == 1:
			root.geometry("800x600+0+0")
		elif current_op == 2:
			root.geometry("400x400+0+0")
		elif current_op == 3:
			root.geometry("500x500+0+0")
		else:
			pass

		reader = Reader(root)
		root.mainloop()
		root.destroy()