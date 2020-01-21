from PIL import Image

im = Image.open('sprites2.png')

j = 27
for i in range(14):
	im.crop((34 * i, 34 * j, 34 * i + 34, 34 * j + 34)).save(f'tmp/{j}{i}.png')
