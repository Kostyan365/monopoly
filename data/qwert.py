from PIL import Image, ImageDraw

# Создаем белый квадрат
img = Image.new('RGBA', (70, 140), 'white')
idraw = ImageDraw.Draw(img)

idraw.rectangle((10, 10, 100, 100), fill='blue')

img.




im = Image.open("kazna.JPG")
size = int(im.size[0])
z=1
x = 0
y = 0
for i in range(2):
    for j in range(1):
        im_crop = im.crop((x, y, x + size, y + size))
        txt = f'kazna{z}.jpg'
        im_crop.save(txt, quality=95)
        x += size
        z+=1
    x = 0
    y += size