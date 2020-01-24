from PIL import Image

im = Image.open('maps/4.png')

w, h = im.size

pix = im.load()

for i in range(w):
	pix[i] = pix[i][-1]
im.show()