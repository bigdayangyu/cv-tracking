from tkinter import *

class Buttons:
	def __init__(self, master):
		frame = Frame(master)
		frame.pack()

		self.printButton = Button(frame, text = "Print msg", command = self.print_button)
		self.printButton.pack(side = LEFT)
		self.quitButton = Button(frame, text = "quit", command = frame.quit)
		self.quitButton.pack(side = LEFT)
	def print_button(self):
		print("what the fuck?")

root = Tk()
b = Buttons(root)
root.mainloop()
