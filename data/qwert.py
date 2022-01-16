from PIL import Image, ImageDraw, ImageFont
import sqlite3
import os


def cut_card(id, img):
    size = int(img.size[0])
    z = 1
    x = 0
    y = 0
    rang = 1
    if img.size == (140, 140):
        rang = 2
        size = size / 2
    for i in range(2):
        for j in range(rang):
            im_crop = img.crop((x, y, x + size, y + size))
            im_crop.save(f'{id}/img{z}.jpg', quality=95)
            x += size
            z += 1
        x = 0
        y += size


def create_card(id, prise, name, orientation, col, col2='white'):
    if (id == 1) or (id == 11) or (id == 21) or (id == 31):
        img = Image.open(f'icon\img{id}.jpg')
        cut_card(id, img)
        return
    col_text = 'black'
    if col == 'black':
        col_text = "white"
    # Создаем белый квадрат
    img = Image.new('RGB', (70, 140), col2)
    idraw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font/Akrobat-ExtraBold.otf", 15, encoding='UTF-8')
    font2 = ImageFont.truetype("font/Akrobat-ExtraBold.otf", 18, encoding='UTF-8')
    idraw.rounded_rectangle((1, 1, 68, 138), radius=5, outline='black', width=1)
    up_text=str(prise) + ' $'
    up_text_coords=(35, 128,)
    if (id == 8) or (id == 23) or (id == 37):
        idraw.rounded_rectangle((1, 1, 68, 138), radius=5, outline='black', width=1, fill=col)
        idraw.rounded_rectangle((5, 5, 65, 135), fill="white",radius=5, outline='black', width=1,)
        up_text = 'ШАНС'
        name=''
        idraw.multiline_text((35, 27,), 'Испытай\nудачу', fill='red', font=font, anchor='ms', spacing=2, align='left')
    elif (id == 8) or (id == 18) or (id == 34):
        idraw.rounded_rectangle((1, 1, 68, 138), radius=5, outline='black', width=1, fill=col)
        idraw.rounded_rectangle((5, 5, 65, 135), fill="#FFFF00",radius=5, outline='black', width=1,)
        up_text = "КАЗНА"
        name=''
        idraw.multiline_text((35, 27,), 'Испытай\nудачу', fill='red', font=font, anchor='ms', spacing=2, align='left')
    elif id == 5:
        idraw.rounded_rectangle((1, 1, 68, 138), radius=5, outline='black', width=1, fill=col)
        up_text = "Плати\n200 $"
        font2 = ImageFont.truetype("font/Akrobat-ExtraBold.otf", 14, encoding='UTF-8')
        up_text_coords = (35, 120,)
    elif id == 38:
        idraw.rounded_rectangle((1, 1, 68, 138), radius=5, outline='black', width=1, fill=col)
        up_text = "Плати\n100 $"
        font2 = ImageFont.truetype("font/Akrobat-ExtraBold.otf", 14, encoding='UTF-8')
        up_text_coords = (35, 120,)
    else:
        idraw.rounded_rectangle((1, 1, 68, 40), fill=col, outline='black', width=1)

    idraw.multiline_text((35, 17,), name, fill=col_text, font=font, anchor='ms', spacing=2, align='left')
    idraw.multiline_text(up_text_coords, up_text, fill='black', font=font2, anchor='ms', spacing=2,
                         align='left', )
    img.paste(Image.open(f'icon\img{id}.jpg'), (10, 55))
    img.save(f'{id}/origin.jpg', quality=95)
    img.show()
    cut_card(id, img)

    if orientation == "left" or orientation == "right":
        if orientation == "left":
            rotate = 90
        else:
            rotate = -90
        for i in range(1, 3):
            img = Image.open(f'{id}/img{i}.jpg')
            im_rotate = img.rotate(rotate)
            im_rotate.save(f'{id}/img{i}.jpg', quality=95)
            img.close()


conn = sqlite3.connect('database/cards.db')
cur = conn.execute("SELECT * FROM tale")
z = cur.fetchall()
conn.close()

for i in range(0, len(z)):
    try:
        os.mkdir(str(z[i][0]))
    except:
        pass

for i in z:
    id = i[0]
    print(id)
    name = i[1].replace(' ', '\n')
    type_card = i[2]
    status = i[3]
    coords = i[4]
    color = i[5]
    zalog = i[6]
    renta1 = i[7]
    renta2 = i[8]
    renta3 = i[9]
    renta4 = i[10]
    renta5 = i[11]
    renta6 = i[12]
    house = i[13]
    hotel = i[14]
    prise = i[15]

    if (type_card == 1) or (type_card == 4) or (type_card == 5) or (
            type_card == 10):  # Старт, Тюрьма, Полиция, Парковка
        create_card(id, prise, name, "vertical", color)
    elif type_card == 2:  # Сектор шанс
        if id == 8 or id == 23:
            create_card(id, prise, name, "vertical", color)
        else:
            create_card(id, prise, name, "right", color)
    elif type_card == 3:  # Сектор казна
        if id == 3:
            create_card(id, prise, name, "vertical", color)
        if id == 18:
            create_card(id, prise, name, "left", color)
        if id == 34:
            create_card(id, prise, name, "right", color)
    elif type_card == 4:  # Сектор тюрьма
        pass
    elif type_card == 5:  # Сектор полиция
        pass
    elif (type_card == 6) or (type_card == 7) or (type_card == 8):  # Строения, Электрокомпании, Порты
        if id in range(1, 11) or id in range(22, 31):
            create_card(id, prise, name, "vertical", color)
        elif id in range(12, 21):
            create_card(id, prise, name, "left", color)
        else:
            create_card(id, prise, name, "right", color)
    elif id == 5:  # Налог
        create_card(id, prise, name, "vertical", color)
    elif type_card == 38:  # Дорогая покупка
        create_card(id, prise, name, "right", color)
