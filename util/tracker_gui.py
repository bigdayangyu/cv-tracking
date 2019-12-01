from tkinter import *
from PIL import Image, ImageTk
from itertools import count

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

class Status_bar:
	def __init__(self, master):
		# anchor the west(lest buttom )
		self.status = Label(root, text = "Loading....", bd = 1, relief = SUNKEN, anchor = W) # bd = borader 
		self.status.pack(side = BOTTOM, fill = X)
class Add_img:
	def __init__(self, master, image_path):
		self.photo = PhotoImage(file = image_path)
		self.label = Label(master, image = self.photo)
		self.label.pack()

class GIF_display(Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

root = Tk()
b = Buttons(root)
c = Status_bar(root)
lbl = GIF_display(root)
lbl.pack()
lbl.load('test.gif')
root.mainloop()