from PIL import Image


for i in range(4, 8):
	im = Image.open(f'maps/{i}.png')
	im = im.transpose(Image.FLIP_LEFT_RIGHT)
	im.save(f'maps/d{i}.png')