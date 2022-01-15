from PIL import Image

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