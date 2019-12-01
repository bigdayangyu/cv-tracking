from PIL import Image
import glob

class CreateGIF:
	'''
		file_path = "./img"
		save_path = "./output"
		file_name = "test"
		gif = CreateGIF(file_path, save_path, file_name)
		gif.create_gif()

	'''
	def __init__(self, file_path, save_path, file_name):
		self.file_path = file_path
		self.save_path = save_path
		self.file_name = file_name

	def create_gif(self, fps):
		frames = []
		
		images = glob.glob(self.file_path + "/*.jpg")
		gif_duration =1 /fps * 1000  #millsec per frame
		print("numbers of frames: ", len(images))
		print("duration: ", gif_duration, " s")
		for i in images:
			new_frame = Image.open(i)
			frames.append(new_frame)

		frames[0].save(self.save_path + self.file_name + ".gif", format = 'GIF', 
						append_images = frames[1:], 
						save_all = True, 
						duration = gif_duration, 
						optimize=True,
						quality=65,
						loop = 0 ) # loop = 0 loop forever, duration in milliseconds

file_path = "./img"
save_path = "./output/"
file_name = "test"
fps = 20
gif = CreateGIF(file_path, save_path, file_name)
gif.create_gif(fps)