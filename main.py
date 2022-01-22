import time

import pygame
import os
import sys
import ctypes
import random
import sqlite3
from collections import deque

list_sound = ['brosok-igralnyih-kostey', 'brosok-igralnyih-kostey-25740', 'igralnaya-kost-upala', 'katyatsya-po-stolu',
              'kubiki-razletelis', 'odin-kubik-brosili-na-stol', 'zvuk-brosaniya-igralnyih-kostey-2-25771']
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
pygame.mixer.pre_init(44100, -16, 1, 512)  # важно прописать до pygame.init()
pygame.init()  # Инициализация конструктора
res = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))  # разрешение экрана
res = (res[0], res[1] - 50)
pygame.display.set_caption('Monopoly')
pygame.display.set_icon(pygame.image.load('data/icons.png'))

screen = pygame.display.set_mode(res, pygame.FULLSCREEN)  # формируем окно приложения
get_width = screen.get_width()
WIDTH = get_width  # ширина экрана
HEIGHT = screen.get_height()  # высота экрана
clock = pygame.time.Clock()
FPS = 25
nominal = [[0, 0, "kletochku.bmp"], [0, 0, "kletochku.bmp"], [0, 0, "kletochku.bmp"], [0, 0, "kletochku.bmp"],
           [1, 5, "img1.bmp"], [5, 1, "img2.bmp"], [10, 2, "img3.bmp"], [20, 1, "img4.bmp"],
           [50, 1, "img5.bmp"], [100, 4, "img6.bmp"], [500, 2, "img7.bmp"], [1000, 0, "img8.bmp"]]

# основной персонаж
pl1 = ['player1/player1_1.png', 'player1/player1_2.png', 'player1/player1_3.png', 'player1/player1_4.png',
       'player1/player1_5.png', 'player1/player1_6.png']
wallet1 = []
card_player1 = []
pl2 = ['player2/player2_1.png', 'player2/player2_2.png', 'player2/player2_3.png', 'player2/player2_4.png',
       'player2/player2_5.png', 'player2/player2_6.png']
wallet2 = []
list_card = []
card_player2 = []
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
money_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_width = 70
tile_height = 70


def load_img(name, color_key=None):
    """Функция для удобства загрузки изображений"""
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# ---------------------------------------------------------------
def terminate():
    """Функция выхода"""
    pygame.quit()
    sys.exit()


# ---------------------------------------------------------------
class Card:
    def __init__(self, *args):
        data = args
        self.id = data[0]
        self.name = data[1]
        self.type_card = data[2]
        self.status = data[3]
        self.coords = eval(data[4])
        self.color = data[5]
        self.zalog = data[6]
        self.renta1 = data[7]
        self.renta2 = data[8]
        self.renta3 = data[9]
        self.renta4 = data[10]
        self.renta5 = data[11]
        self.renta6 = data[12]
        self.house = data[13]
        self.hotel = data[14]
        self.prise = data[15]
        self.sprite = data[16]


# ---------------------------------------------------------------
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(tile_width * pos_x + (WIDTH / 2 - 455), tile_height * pos_y + 100)


# ---------------------------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player_image):
        super().__init__(player_group, all_sprites)
        self.images = player_image
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect().move(tile_width * pos_x + (WIDTH / 2 - 455) + 15, tile_height * pos_y + 105)
        self.pos = (pos_x, pos_y)

    def update(self):
        """Mетод, анимирует спрайт"""
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def move(self, pos_x, pos_y):
        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + (WIDTH / 2 - 455) + 15,
                                               tile_height * self.pos[1] + 105)


def generate_player(data):
    images = [load_img(i) for i in data]
    return images


class Tablo(pygame.Surface):
    def __init__(self, ):
        super().__init__((630, 100))
        self.fon = pygame.transform.scale(load_img('svetlo-krasnii-fon.jpg'), (WIDTH, HEIGHT))
        self.blit(self.fon, (0, 0))

    def reader(self, message):
        self.fon = pygame.transform.scale(load_img('svetlo-krasnii-fon.jpg'), (WIDTH, HEIGHT))
        self.blit(self.fon, (0, 0))
        pygame.display.update()
        font = pygame.font.Font('data/font/Akrobat-ExtraBold.otf', 16)
        text_coord = 5
        for line in message:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.blit(string_rendered, intro_rect)

        pygame.display.update()


# ---------------------------------------------------------------
class InfoWindow(pygame.Surface):
    def __init__(self, ):
        super().__init__((250, 570))
        self.fon = pygame.transform.scale(load_img('svetlo-krasnii-fon.jpg'), (WIDTH, HEIGHT))
        self.blit(self.fon, (0, 0))

    def reader(self, *args):
        data = args[0]

        if not data:
            self.blit(self.fon, (0, 0))
        elif data.type_card == 6:
            text = [data.name.upper(), "",
                    "Право собственности",
                    f"РЕНТА БЕЗ СТРОЕНИЙ                       {data.renta1} $",
                    f"-1 дом                                                     {data.renta2} $",
                    f"-2 дома                                                 {data.renta3} $",
                    f"-3 дома                                                {data.renta4} $",
                    f"-4 дома                                                {data.renta5} $",
                    f"РЕНТА С ОТЕЛЕМ                              {data.renta6} $",
                    "--------------------------------------------",
                    "Если игроку принадлежит все",
                    "имущество одной цветовой группы,",
                    "рента удваивается",
                    "--------------------------------------------",
                    f"Постройка дома                              {data.house} $",
                    f"Постройка отеля                             {data.hotel} $",
                    f"                                                        + 4 дома",
                    f"Залог                                                    {data.zalog} $", ]
            self.funct(text, data.id, (185, 15))

        elif data.type_card == 1:
            text = [data.name.upper(), "",
                    "Вы пересекли ",
                    "сектор СТАРТ,",
                    "--------------------------------------------",
                    "банк вам выплачивает",
                    "- 200 $"]
            self.funct(text, data.id, (55, 270))

        elif (data.type_card == 2) or (data.type_card == 3):  # Шанс, Касса
            text = self.generate_text(data.type_card)
            self.funct(text, data.id, (185, 15))
        elif data.type_card == 8:  # Порты
            text = [data.name.upper(), "",
                    "Право собственности",
                    f"-1 порт                                                     {data.renta1} $",
                    f"-2 порта                                                 {data.renta2} $",
                    f"-3 порта                                                {data.renta3} $",
                    f"-4 порта                                                {data.renta4} $",
                    "--------------------------------------------",
                    "", "", "", "", "", "", "", "",
                    f"Залог                                                    {data.zalog} $", ]
            self.funct(text, data.id, (185, 15))

        elif data.type_card == 4:  # Тюрьма
            text = ["ТЮРЬМА", "",
                    "Вы просто",
                    "зашли",
                    "ненадолго",
                    "-----------",
                    "вы не платите ",
                    "никакого штрафа"]
            self.funct(text, data.id, (55, 310))

        elif data.type_card == 5:  # Полиция
            text = ["ПОЛИЦИЯ", "",
                    "Вы арестованы",
                    "и не получаете",
                    "200$ за проход",
                    "поля СТАРТ",
                    "-----------",
                    "Отправляйтесь ",
                    "в тюрьму"]
            self.funct(text, data.id, (55, 310))

        elif data.type_card == 7:  # Энергокомпании
            text = [data.name.upper(), "",
                    "Право собственности",
                    "Рента равна",
                    "значению брошеных",
                    f"камней      Х на {data.renta1} $",
                    "---------------------------",
                    "Если обе компании",
                    "услуг в",
                    "собственности",
                    "---------------------------",
                    "Рента равна",
                    "значению брошеных",
                    f"камней      Х на {data.renta1} $", ]
            self.funct(text, data.id, (185, 15))
        elif data.type_card == 10:  # Парковка
            text = ["БЕСПЛАТНАЯ",
                    "ПАРКОВКА", "",
                    "Пропустите",
                    "один",
                    "ход",
                    "-----------", ]
            self.funct(text, data.id, (55, 270))
        elif data.type_card == 9:  # Налоги
            text = [data.name.upper(), "",
                    "------------",
                    f"Заплатите",
                    f"{data.renta1} $", ]
            self.funct(text, data.id, (185, 15))

    def generate_text(self, type):
        new_txt = self._s(type)
        print(new_txt)
        return new_txt

    def _s(self, typ):
        x = random.randrange(1, 17)
        table = 0
        t = 0
        if typ == 2:
            table = 'chance'
            t = 'ШАНС'
        elif typ == 3:
            table = 'treasury'
            t = 'КАЗНА'
        conn = sqlite3.connect('data/database/cards.db')
        cur = conn.execute(f"SELECT * FROM {table} WHERE id={x}")
        z = cur.fetchall()
        conn.close()
        a = self._z(z[0][1].split())
        a.insert(0, f'{t}')
        if z[0][2] == None:
            b = ['']
        else:
            b = self._z(z[0][2].split())
        b.insert(0, '----------------')
        a.extend(b)
        return a

    def _z(self, txt):
        w = []
        flag = False
        for i in range(len(txt)):
            if flag:
                flag = False
                continue
            if i == len(txt) - 1:
                w.append(txt[i])
                break
            else:
                w.append(txt[i] + ' ' + txt[i + 1])
                flag = True
        return w

    def funct(self, text, id, cords):
        font = pygame.font.Font('data/font/Akrobat-ExtraBold.otf', 16)
        text_coord = 5
        for line in text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.blit(string_rendered, intro_rect)
        self.image = load_img(f'icon/img{id}.jpg')
        self.blit(self.image, cords)
        pygame.display.update()


class Button:
    def __init__(self, text, cord_rect, x=0, y=0):
        self.cord_rect = cord_rect
        self.cord_text = (cord_rect[0] + x, cord_rect[1] + y)
        color = (255, 255, 255)  # белый цвет
        self.color_light = (170, 170, 170)  # светлый оттенок кнопки
        self.color_dark = (100, 100, 100)  # темный оттенок кнопки
        smallfont = pygame.font.SysFont('Corbel', 25)  # Определение шрифта
        self.text_but = smallfont.render(text, True, color)  # рендеринг текста, написанного в этот шрифт
        self.left = cord_rect[0]
        self.right = cord_rect[0] + cord_rect[2]
        self.up = cord_rect[1]
        self.down = cord_rect[1] + cord_rect[3]

    def update(self):
        pygame.draw.rect(screen, self.color_dark, self.cord_rect, border_radius=5)
        screen.blit(self.text_but, self.cord_text)

    def focus(self):
        pygame.draw.rect(screen, self.color_light, self.cord_rect, border_radius=5)
        screen.blit(self.text_but, self.cord_text)


# ---------------------------------------------------------------
class Dice:
    def __init__(self):

        self.surf_dice = pygame.Surface((130, 570))
        self.surf_dice.fill("white")
        screen.blit(self.surf_dice, (WIDTH / 2 - 65, 240))

    def play(self):
        dice1 = random.randrange(1, 7)  # Значение кости1
        dice2 = random.randrange(1, 7)  # Значение кости2
        dice1_path = random.randrange(1, 9)  # Путь кости1
        dice2_path = random.randrange(1, 9)  # Путь кости2
        coords_1 = 570
        coords_2 = 570
        rang = dice1_path
        if dice2_path > dice1_path:
            rang = dice2_path
        flag1 = False
        flag2 = False
        temp = [0, 0]
        dice_img = dice_img2 = 0

        for i in range(1, rang):
            self.surf_dice.fill("white")  # Очищаем сурф
            if i >= dice1_path - 1:
                if not flag1:
                    temp[0] = coords_1
                    flag1 = True
                    dice_img = load_img(f"dice/dice{dice1}.png")
                dice_rect = dice_img.get_rect(bottomleft=(0, temp[0]))
                self.surf_dice.blit(dice_img, dice_rect)
            else:
                dice_img = load_img(f"dice/dice{random.randrange(1, 7)}.png")
                dice_rect = dice_img.get_rect(bottomleft=(0, coords_1))
                self.surf_dice.blit(dice_img, dice_rect)

            if i >= dice2_path - 1:
                if not flag2:
                    temp[1] = coords_2
                    dice_img2 = load_img(f"dice/dice{dice2}.png")
                    flag2 = True
                dice_rect2 = dice_img2.get_rect(bottomright=(130, temp[1]))
                self.surf_dice.blit(dice_img2, dice_rect2)
            else:
                dice_img2 = load_img(f"dice/dice{random.randrange(1, 7)}.png")
                dice_rect2 = dice_img2.get_rect(bottomright=(130, coords_2))
                self.surf_dice.blit(dice_img2, dice_rect2)

            screen.blit(self.surf_dice, (WIDTH / 2 - 65, 240))
            pygame.display.flip()
            s_catch = pygame.mixer.Sound(f'sound/{random.choice(list_sound)}.ogg')
            s_catch.play()
            pygame.time.wait(100)
            coords_1 -= 65
            coords_2 -= 65
        font = pygame.font.Font('data/font/Akrobat-ExtraBold.otf', 30)
        line = f"    {dice1}         {dice2}"
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        self.surf_dice.blit(string_rendered, intro_rect)
        screen.blit(self.surf_dice, (WIDTH / 2 - 65, 240))

        return [dice1, dice2]


# ---------------------------------------------------------------
class Money(pygame.Surface):
    def __init__(self, data, pos_x, pos_y):
        super().__init__((120, 230))
        # print(data, pos_x, pos_y)
        self.nominal = data[0]
        self.quantity = data[1]
        self.image = load_img(f'money/{data[2]}')
        self.rect = self.image.get_rect(
            topleft=(pos_x, pos_y))  # получаем ссылку на размеры этой области в виде экземпляра класса Rect


def gen_money(x, y, player):
    tmp = 0
    for i in range(3):
        for j in range(4):
            z = Money(nominal[tmp], x, y)
            z.scroll(x, y)
            screen.blit(z.image, z.rect)
            if player == 1:
                wallet1.append(z)
            if player == 2:
                wallet2.append(z)
            tmp += 1
            x += 82
        if player == 1:
            x = WIDTH // 2 - 455 - 328
            y += 200
        if player == 2:
            x = WIDTH // 2 + 455
            y += 200


# ---------------------------------------------------------------
def generate_level():
    conn = sqlite3.connect('data/database/cards.db')
    cur = conn.execute("SELECT * FROM tale")
    z = cur.fetchall()
    conn.close()
    for data in (z):
        list_card.append(Card(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9],
                              data[10], data[11], data[12], data[13], data[14], data[15],
                              [Tile(load_img(f'{data[0]}/img{enum}.jpg'), *_) for enum, _ in
                               enumerate(eval(data[4]), start=1)]))


# ---------------------------------------------------------------
class CardPlayer(pygame.Surface):
    def __init__(self, pos_x, pos_y):
        super().__init__((70, 140))
        print(pos_x, pos_y)
        self.image = load_img("kletochki2.bmp")
        self.rect = self.image.get_rect(
            topleft=(pos_x, pos_y))  # получаем ссылку на размеры этой области в виде экземпляра класса Rect


def card_player(x, y, player):
    tmp = 0
    for i in range(3):
        for j in range(7):
            z = CardPlayer(x, y)
            z.scroll(x, y)
            screen.blit(z.image, z.rect)
            if player == 1:
                card_player1.append(z)
            else:
                card_player2.append(z)
            tmp += 1
            x += 70
        if player == 1:
            x = WIDTH // 2 - 455 - 490
            y += 140
        else:
            x = WIDTH // 2 + 455
            y += 140
    for i in range(3):
        for j in range(2):
            if player == 1:
                z = CardPlayer(x, y)
                card_player1.append(z)
            else:
                z = CardPlayer(x + 350, y)
                card_player2.append(z)
            z.scroll(x, y)
            screen.blit(z.image, z.rect)
            tmp += 1
            x += 70
        if player == 1:
            x = WIDTH // 2 - 455 - 490
            y += 140
        else:
            x = WIDTH // 2 + 455
            y += 140


# ---------------------------------------------------------------
def start_screen():
    "Заставка"
    pygame.mixer.music.load("3d20874f20174bd.mp3")
    # pygame.mixer.music.play(-1)
    fon = pygame.transform.scale(load_img('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    font2 = pygame.font.Font(None, 200)
    text = font2.render("Монополия", True, (241, 0, 0))
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT // 6))
    screen.blit(text, text_rect)

    color = (255, 255, 255)  # белый цвет
    color_light = (170, 170, 170)  # светлый оттенок кнопки
    color_dark = (100, 100, 100)  # темный оттенок кнопки
    smallfont = pygame.font.SysFont('Corbel', 35)  # Определение шрифта
    text_nev_game = smallfont.render('Новая игра', True, color)  # рендеринг текста, написанного в этот шрифт
    text_quit = smallfont.render('Выход', True, color)
    while True:
        mouse = pygame.mouse.get_pos()  # хранит координаты (X, Y)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
                # проверяет, нажала ли мышь
            if ev.type == pygame.MOUSEBUTTONDOWN:

                if WIDTH / 2 - 100 <= mouse[0] <= WIDTH / 2 + 100 and HEIGHT / 1.5 <= mouse[1] <= HEIGHT / 1.5 + 40:
                    return  # начинаем игру
                if WIDTH / 2 - 100 <= mouse[0] <= WIDTH / 2 + 100 and HEIGHT / 1.5 + 60 <= mouse[
                    1] <= HEIGHT / 1.5 + 60 + 40:
                    terminate()  # Если мышь нажала на кнопку игра прекращена

        # Если мышь наведена на кнопку меняем цвет на светлый
        if WIDTH / 2 - 100 <= mouse[0] <= WIDTH / 2 + 100 and HEIGHT / 1.5 <= mouse[1] <= HEIGHT / 1.5 + 40:
            pygame.draw.rect(screen, color_light, [WIDTH / 2 - 100, HEIGHT / 1.5, 200, 40])
        else:
            pygame.draw.rect(screen, color_dark, [WIDTH / 2 - 100, HEIGHT / 1.5, 200, 40])

        if WIDTH / 2 - 100 <= mouse[0] <= WIDTH / 2 + 100 and HEIGHT / 1.5 + 60 <= mouse[1] <= HEIGHT / 1.5 + 60 + 40:
            pygame.draw.rect(screen, color_light, [WIDTH / 2 - 100, HEIGHT / 1.5 + 60, 200, 40])
        else:
            pygame.draw.rect(screen, color_dark, [WIDTH / 2 - 100, HEIGHT / 1.5 + 60, 200, 40])

        # Нанося текст на нашу кнопку
        screen.blit(text_nev_game, (WIDTH / 2 - 85, HEIGHT / 1.5))
        screen.blit(text_quit, (WIDTH / 2 - 85, HEIGHT / 1.5 + 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# ---------------------------------------------------------------
start_screen()  # Заставка
generate_level()  # Генерируем игровое поле
player1 = Player(11, 11, generate_player(pl1))  # Создаем 1 игрока
player2 = Player(11, 12, generate_player(pl2))  # Создаем 2 игрока
d = deque(list(range(0, 40)))  # Очередь из карточек
fon = pygame.transform.scale(load_img('fon2.jpg'), (WIDTH, HEIGHT))
screen.blit(fon, (0, 0))
but = Button("Ход", (WIDTH / 2 - 65, 810, 130, 60), 45, 18)
but_exit = Button("Выход", (WIDTH / 2 + 315, 0, 140, 100), 37, 36)
but_razmen1 = Button("Размен", (WIDTH / 2 - 190, 810, 125, 60), 25, 18)
but_oplata1 = Button("Оплатить", (WIDTH / 2 - 315, 810, 125, 60), 7, 18)
but_razmen2 = Button("Размен", (WIDTH / 2 + 65, 810, 125, 60), 25, 18)
but_oplata2 = Button("Оплатить", (WIDTH / 2 + 190, 810, 125, 60), 7, 18)
gen_money(WIDTH // 2 - 455 - 328, HEIGHT - 600, 1)
gen_money(WIDTH // 2 + 455, HEIGHT - 600, 2)
card_player(WIDTH // 2 - 455 - 490, 0, 1)
card_player(WIDTH // 2 + 455, 0, 2)
dice = Dice()
info_window = InfoWindow()
info_window2 = InfoWindow()
info_window.reader(list_card[0])  #:TODO
tablo = Tablo()

message = [['НОВАЯ ИГРА, разыграем право первого хода', 'игрок слева - пробел, игрок справа - мышь'],
           ['Игрок слева сделал ход', 'ждем правого игрока'], ['Игрок справа сделал ход', 'ждем левого игрока'],
           ['Первым ходит игрок слева'], ['Первым ходит игрок справа'],
           ['Выпало одинаковое количество очков', 'придется перебросить']]
tablo.reader(message[0])

dt = 0
timer = 0
running = True
active_left = False
active_right = False


def play():
    global active_left, active_right
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and active_left == False:
                if event.key == pygame.K_SPACE:
                    active_left = sum(dice.play())
                    tablo.reader(message[1])

            if event.type == pygame.MOUSEBUTTONDOWN and active_right == False:
                if but.left <= mouse[0] <= but.right and but.up <= mouse[1] <= but.down:
                    active_right = sum(dice.play())
                    tablo.reader(message[2])

                if but_exit.left <= mouse[0] <= but_exit.right and but_exit.up <= mouse[1] <= but_exit.down:
                    terminate()  # Если мышь нажала на кнопку игра прекращена

        if active_right and active_left:
            if active_right > active_left:
                tablo.reader(message[4])
                active_left = False
                active_right = True
                return
            elif active_right < active_left:
                tablo.reader(message[3])
                active_left = True
                active_right = False
                return
            elif active_right == active_left:
                tablo.reader(message[5])
                active_left = False
                active_right = False

        if but.left <= mouse[0] <= but.right and but.up <= mouse[1] <= but.down:  # Кнопка ход
            but.focus()
        else:
            but.update()
        if but_exit.left <= mouse[0] <= but_exit.right and but_exit.up <= mouse[1] <= but_exit.down:  # Кнопка выход
            but_exit.focus()
        else:
            but_exit.update()
        tiles_group.draw(screen)
        player_group.update()
        player_group.draw(screen)
        money_group.draw(screen)
        screen.blit(info_window, (WIDTH / 2 - 315, 240))
        screen.blit(info_window2, (WIDTH / 2 + 65, 240))
        screen.blit(tablo, (WIDTH / 2 - 315, 0))
        clock.tick(FPS)
        pygame.display.flip()


def move_handler(player):  # Обработчик хода
    tmp = sum(dice.play())
    info_window.reader(False)
    for i in range(tmp):
        z = d.popleft()
        _index = d[0]
        # print(list_card[_index].coords[0])
        x, y = list_card[_index].coords[0]
        if player == 1:
            player1.move(x, y)
        else:
            player2.move(x, y)
        clock.tick(5)
        tiles_group.draw(screen)
        player_group.update()
        player_group.draw(screen)
        pygame.display.flip()
        d.append(z)
        if tmp == i + 1:
            info_window.reader(list_card[_index])


def game(player):
    global active_left, active_right
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if but_exit.left <= mouse[0] <= but_exit.right and but_exit.up <= mouse[1] <= but_exit.down:
                terminate()  # Если мышь нажала на кнопку игра прекращена
            if (but.left <= mouse[0] <= but.right and but.up <= mouse[1] <= but.down) and (
                    player == 2):  # Если нажата кнопка ход
                move_handler(player)
                active_left = True
                active_right = False

        if (event.type == pygame.KEYDOWN) and (player == 1):
            if event.key == pygame.K_SPACE:  # Если нажата кнопка ход
                move_handler(player)
                active_left = False
                active_right = True


while True:
    mouse = pygame.mouse.get_pos()
    if not active_right and not active_left:  # Первый запуск
        play()

    if but.left <= mouse[0] <= but.right and but.up <= mouse[1] <= but.down:  # Кнопка ход
        but.focus()
    else:
        but.update()
    if but_exit.left <= mouse[0] <= but_exit.right and but_exit.up <= mouse[1] <= but_exit.down:  # Кнопка выход
        but_exit.focus()
    else:
        but_exit.update()
    if but_razmen1.left <= mouse[0] <= but_razmen1.right and but_razmen1.up <= mouse[
        1] <= but_razmen1.down:  # Кнопка Pазмен1
        but_razmen1.focus()
    else:
        but_razmen1.update()
    if but_oplata1.left <= mouse[0] <= but_oplata1.right and but_oplata1.up <= mouse[
        1] <= but_oplata1.down:  # Кнопка Оплата1
        but_oplata1.focus()
    else:
        but_oplata1.update()
    if but_razmen2.left <= mouse[0] <= but_razmen2.right and but_razmen2.up <= mouse[
        1] <= but_razmen2.down:  # Кнопка Pазмен2
        but_razmen2.focus()
    else:
        but_razmen2.update()
    if but_oplata2.left <= mouse[0] <= but_oplata2.right and but_oplata2.up <= mouse[
        1] <= but_oplata2.down:  # Кнопка Оплата1
        but_oplata2.focus()
    else:
        but_oplata2.update()

    if active_left:
        game(1)

    elif active_right:
        game(2)

    tiles_group.draw(screen)
    player_group.update()
    player_group.draw(screen)
    money_group.draw(screen)
    screen.blit(info_window, (WIDTH / 2 - 315, 240))
    screen.blit(info_window2, (WIDTH / 2 + 65, 240))
    screen.blit(tablo, (WIDTH / 2 - 315, 0))
    clock.tick(FPS)
    pygame.display.flip()
