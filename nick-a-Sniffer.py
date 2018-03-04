#!/usr/bin/env python

import os
from Tkinter import *
from PIL import Image, ImageTk
import tkFont
import subprocess
import sys


class Window(Frame):

	# Initialize
	def __init__(self, master = None):
		Frame.__init__(self, master)

		self.master = master
		self.init_window()

	# Initialize
	def init_window(self):
		self.master.title("Nick-a-Sniffer")
		self.pack(fill=BOTH, expand=1,)

		# SET FONT
		helv10 = tkFont.Font(family='Courier', size=10, weight='normal')

		# ADD MENU AND DROP DOWNS
		menu = Menu(self.master, font=helv10, bd=0.5)
		self.master.config(menu=menu)

		exits = Menu(menu, tearoff=0)
		exits.add_command(label='Exit', font=helv10, command=self.client_exit)
		menu.add_cascade(label='Exit', menu=exits)

		clearscreen = Menu(menu, tearoff=0)
		clearscreen.add_command(label='Clear', font=helv10, command=self.cleartext)
		menu.add_cascade(label='Clearscreen', menu=clearscreen)

		info = Menu(menu, tearoff=0)
		info.add_command(label='Info', font=helv10, command=self.client_info)
		menu.add_cascade(label='About', menu=info)

		# RIGHT PANEL LIST BOX, CHANGE WIDTH FOR DIFFERENT SCREEN RESOLUTIONS
		self.lb_tasks = Listbox(self, bg="white", width=68, height=25, font=helv10)
		self.lb_tasks.grid(row=0, column=1, rowspan=4,)
		
		# SCROLLBAR
		self.sb1 = Scrollbar(self)
		self.sb1.grid(row=0,column=2, rowspan=4, ipady=150)
		self.lb_tasks.configure(yscrollcommand=self.sb1.set)
		self.sb1.configure(command=self.lb_tasks.yview)
		
		# LEFT PANEL, CHANGE PADY HERE FOR DIFFERENT SCREEN RESOLUTIONS
		labela = Label(self, relief='flat')
		labela.grid(row=0, column=0)
		labela.config(text="This program uses stuff to do an arp scan of your local network\nStuff must be installed for this to work")
		labela.config(wraplength=270, justify=CENTER, padx=25, pady=20, font=('Purisa', 12,))
		
		# BUTTON RELIEF IS RAISED, SOLID, GROOVE, FLAT, SUNKEN, OR RIDGE
		self.scanbutton = Button(self, text="Scan", font=helv10, width=20, padx=2, pady=10, command=self.sctofile)
		self.scanbutton.grid(row=1, column=0, sticky=S)
		self.cdbbutton = Button(self, text="View Database", font=helv10, width=20, padx=2, pady=10, command=self.client_db)
		self.cdbbutton.grid(row=2, column=0, sticky=N)

		# IMAGE
		load = Image.open('n-sniff.png')
		render = ImageTk.PhotoImage(load)
		img = Label(self, image=render)
		img.image = render
		img.grid(row=3, column=0)

		labelb = Label(self, relief='flat')
		labelb.grid(row=4, column=0, columnspan=2)
		labelb.config(text="Click Scan to see who is on your network\nYou are the master of your own database")
		labelb.config(justify=CENTER, pady=15, font=('Purisa', 12,))
	
	# VIEW DATABASE	
	def client_db(self):
		with open('identifiedDB.txt') as fo:
			for line in fo:
				self.write(str(line) + '\n')

	# WRITE SCAN RESULTS TO FILE
	# SUBPROCESS NEEDS EXACT FILE PATH TO BASH SCRIPT
	def sctofile(self):
		lines = open('arpNEW.txt', 'w')
		row = subprocess.check_output(["/home/andy/Desktop/anick/arpSCAN.sh"])
		lines.write(row)
		lines.close()

		self.results()
	
	# SHOW RESULTS IN MAIN WINDOW	
	def results(self):
		with open('arpNEW.txt') as fo:
			for line in fo:
				self.write(str(line) + '\n')
		
		self.danger()

	# PARSE TEXTFILE, ADD TO SET THEN COMPARE SETS
	def danger(self):		
		f3 = set()

		with open('arpNEW.txt') as f1:
			next(f1)
			next(f1)
			next(f1)
			for line in f1:
				mack = line[12:].strip()
				f3.add(mack)

		self.write(str('------- NOT ON DATABASE -------'))
		f2 =  set(open('identifiedMACS.txt').read().split())

		for mack in (f3 - f2):
			self.write('DANGER ------> ' + mack)

	# INFO
	def client_info(infotext):
		popup = Tk()
		popup.wm_title("Information")		
		infotext = Label(popup, text="\nAuthored by A.Greenhalgh\n\nLinux Mint using python 2.7\n\n")
		infotext.config(width=60, bg="white", font=("Courier", 10))
		infotext.pack()
		butt1 = Button(popup, text="Ok", command=popup.destroy)
		butt1.pack(pady=10)
		popup.mainloop()

	# EXIT PROGRAM
	def client_exit(self):
		exit()

	# WRITE TO LISTBOX
	def write(self, text):
		self.lb_tasks.insert(END,str(text))
		self.update_idletasks()

	# CLEAR
	def cleartext(self):
		self.lb_tasks.delete(0, END)

root = Tk()
root.geometry("1000x700")
root.resizable(0, 0) # LOCKS THE WINDOW SIZE
app = Window(root)
root.mainloop()
