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
width = screen.get_width()  # ширина экрана
height = screen.get_height()  # высота экрана
clock = pygame.time.Clock()
FPS = 15

# основной персонаж
pl1 = ['player1/player1_1.png', 'player1/player1_2.png', 'player1/player1_3.png', 'player1/player1_4.png',
       'player1/player1_5.png', 'player1/player1_6.png']
pl2 = ['player2/player2_1.png', 'player2/player2_2.png', 'player2/player2_3.png', 'player2/player2_4.png',
       'player2/player2_5.png', 'player2/player2_6.png']
list_card = []
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_width = 70
tile_height = 70


def load_img(name, colorkey=None):
    """Функция для удобства загрузки изображений"""
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    """Функция выхода"""
    pygame.quit()
    sys.exit()


class Card:
    def __init__(self, *args):
        i = args
        self.id = i[0]
        self.name = i[1]
        self.type_card = i[2]
        self.status = i[3]
        self.coords = eval(i[4])
        self.color = i[5]
        self.zalog = i[6]
        self.renta1 = i[7]
        self.renta2 = i[8]
        self.renta3 = i[9]
        self.renta4 = i[10]
        self.renta5 = i[11]
        self.renta6 = i[12]
        self.house = i[13]
        self.hotel = i[14]
        self.prise = i[15]
        self.sprite = i[16]


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(tile_width * pos_x + (width / 2 - 455), tile_height * pos_y + 100)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player_image):
        super().__init__(player_group, all_sprites)
        self.images = player_image
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect().move(tile_width * pos_x + (width / 2 - 455) + 15, tile_height * pos_y + 105)
        self.pos = (pos_x, pos_y)

    def update(self):
        """Mетод, анимирует спрайт"""
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + (width / 2 - 455) + 15,
                                               tile_height * self.pos[1] + 105)


class Info_window(pygame.Surface):
    def __init__(self, ):
        super().__init__((250, 570))
        self.fon = pygame.transform.scale(load_img('fon.jpg'), (width, height))
        self.blit(self.fon, (0, 0))

    def reader(self, *args):
        print(type(args[0]))
        data = args[0]

        if data==False:
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
                    f"Залог                                                    {data.zalog} $",]
            self.funct(text,data.id,(185, 15))

        elif data.type_card == 1:
            text = [data.name.upper(), "",
                    "Вы пересекли ",
                    "сектор СТАРТ,",
                    "--------------------------------------------",
                    "банк вам выплачивает",
                    "- 200 $"]
            self.funct(text,data.id,(55, 270))

    def funct(self,text,id,cords):
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




info_window = Info_window()


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


def start_screen():
    pygame.mixer.music.load("3d20874f20174bd.mp3")
    # pygame.mixer.music.play(-1)
    fon = pygame.transform.scale(load_img('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    font2 = pygame.font.Font(None, 200)
    text = font2.render("Монополия", True, (241, 0, 0))
    text_rect = text.get_rect(center=(width / 2, height // 6))
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

                if width / 2 - 100 <= mouse[0] <= width / 2 + 100 and height / 1.5 <= mouse[1] <= height / 1.5 + 40:
                    return  # начинаем игру
                if width / 2 - 100 <= mouse[0] <= width / 2 + 100 and height / 1.5 + 60 <= mouse[
                    1] <= height / 1.5 + 60 + 40:
                    terminate()  # Если мышь нажала на кнопку игра прекращена

        # Если мышь наведена на кнопку меняем цвет на светлый
        if width / 2 - 100 <= mouse[0] <= width / 2 + 100 and height / 1.5 <= mouse[1] <= height / 1.5 + 40:
            pygame.draw.rect(screen, color_light, [width / 2 - 100, height / 1.5, 200, 40])
        else:
            pygame.draw.rect(screen, color_dark, [width / 2 - 100, height / 1.5, 200, 40])

        if width / 2 - 100 <= mouse[0] <= width / 2 + 100 and height / 1.5 + 60 <= mouse[1] <= height / 1.5 + 60 + 40:
            pygame.draw.rect(screen, color_light, [width / 2 - 100, height / 1.5 + 60, 200, 40])
        else:
            pygame.draw.rect(screen, color_dark, [width / 2 - 100, height / 1.5 + 60, 200, 40])

        # Нанося текст на нашу кнопку
        screen.blit(text_nev_game, (width / 2 - 85, height / 1.5))
        screen.blit(text_quit, (width / 2 - 85, height / 1.5 + 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def generate_player(data):
    images = [load_img(i) for i in data]
    return images


class Dice:
    def __init__(self):
        self.s_catch = pygame.mixer.Sound(f'sound/{random.choice(list_sound)}.ogg')
        self.dice1 = random.randrange(1, 7)
        self.dice2 = random.randrange(1, 7)

    def play(self):
        self.s_catch.play()
        return self.dice1 + self.dice2


start_screen()
generate_level()
player1 = Player(11, 11, generate_player(pl1))
player2 = Player(11, 12, generate_player(pl2))
print(player1.pos)
print(player2.pos)
info_window.reader(list_card[0])
d = deque(list(range(0, 40)))
fon = pygame.transform.scale(load_img('fon2.jpg'), (width, height))

# движение персонажа
# левая белая поверхность,
# равная половине окна
surf_left = pygame.Surface(
    (width // 2, height))
surf_left.fill("white")

# правая черная поверхность,
# равная другой половине окна
surf_right = pygame.Surface(
    (width // 2, height))

# размещаем поверхности на главной,
# указывая координаты
# их верхних левых углов
screen.blit(surf_left, (0, 0))
screen.blit(surf_right, (width // 2, 0))
dt = 0
timer = 0
running = True
while running:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():  # обращаемся к очереди событий, где event-событие из очереди(итерируемый объект)
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                _=Dice().play()
                info_window.reader(False)
                for i in range(_):

                    z = d.popleft()
                    _index = d[0]

                    # print(list_card[_index].coords[0])
                    x, y = list_card[_index].coords[0]
                    player1.move(x, y)
                    clock.tick(5)
                    tiles_group.draw(screen)
                    player_group.update()
                    player_group.draw(screen)
                    pygame.display.flip()
                    d.append(z)
                    if _==i+1:
                        info_window.reader(list_card[_index])

        if width / 2 - 100 <= mouse[0] <= width / 2 + 100 and height / 1.5 + 60 <= mouse[1] <= height / 1.5 + 60 + 40:
            terminate()  # Если мышь нажала на кнопку игра прекращена

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if timer == 0:  # First mouse click.
                    timer = 0.001  # Start the timer.
                # Нажмите еще раз до 0,5 секунды, чтобы дважды щелкнуть.
                elif timer < 0.1:
                    print('double click')
                    pygame.display.iconify()
                    timer = 0
    # Увеличение таймера после того, как мышь нажал первый раз.
    if timer != 0:
        timer += dt
        # Сброс через 0,5 секунды.
        if timer >= 0.1:
            timer = 0

        # dt == time in seconds since last tick.
        # / 1000 to convert milliseconds to seconds.
    dt = clock.tick(30) / 1000

    # screen.blit(fon, (0, 0))
    tiles_group.draw(screen)
    player_group.update()
    player_group.draw(screen)
    surf_left.fill("white")
    screen.blit(info_window, (50, 50))
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
