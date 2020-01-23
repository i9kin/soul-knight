from PIL import Image

im = Image.open('tiny-16-basic.png')

for j in range(16):
	for i in range(16):
		im.crop((32 * i, 32 * j, 32 * i + 32,  32 * j + 32)).save(f'maps/{j * 32 + i}.png')
