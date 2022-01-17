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
pygame.display.set_caption('Monopoly')
screen = pygame.display.set_mode(res)  # открывает окно
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


def dice():
    z = random.choice(list_sound)
    s_catch = pygame.mixer.Sound(f'sound/{z}.ogg')
    s_catch.play()









"""class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):

        x1 = width / 2 - 315
        y1 = 240
        pygame.draw.rect(screen, (255, 0, 0), (width / 2 - 455, 100, 910, 910), 2)
        pygame.draw.rect(screen, (255, 0, 0), (width / 2 - 315, 240, 630, 630), 2)
        for i in range(10):
            pygame.draw.line(screen, (255, 0, 0), [x1, 100], [x1, 240], 2)
            pygame.draw.line(screen, (255, 0, 0), [x1, 870], [x1, 1010], 2)
            x1 += 70
            pygame.draw.line(screen, (255, 0, 0), [width / 2 - 455, y1], [width / 2 - 315, y1], 2)
            pygame.draw.line(screen, (255, 0, 0), [width / 2 + 315, y1], [width / 2 + 455, y1], 2)
            y1 += 70

            # pygame.draw.rect(screen, (255, 255, 255), (coord_x, coord_y, self.cell_size, self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        ceil_x = (mouse_pos[0] - self.left) // self.cell_size
        ceil_y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= ceil_x < self.width and 0 <= ceil_y < self.height:
            return ceil_x, ceil_y
        return None
    def on_click(self, ceil):
        print(ceil)"""
start_screen()
generate_level()
player1 = Player(11, 11, generate_player(pl1))
player2 = Player(11, 12,generate_player(pl2))
print(player1.pos)
print(player2.pos)








rand = 6
d = deque(list(range(0, 40)))

dice()
fon = pygame.transform.scale(load_img('fon2.jpg'), (width, height))
# board = Board(13, 13)
# board.set_view(width / 2 - 455, 100, 70)
# движение персонажа



running = True
while running:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:

                for i in range(6):
                    z = d.popleft()
                    _index = d[0]
                    print(list_card[_index].coords[0])
                    x, y = list_card[_index].coords[0]
                    player1.move(x, y)
                    d.append(z)
        # if event.type == pygame.MOUSEBUTTONDOWN:
        # board.get_click(event.pos)
        if width / 2 - 100 <= mouse[0] <= width / 2 + 100 and height / 1.5 + 60 <= mouse[1] <= height / 1.5 + 60 + 40:
            terminate()  # Если мышь нажала на кнопку игра прекращена
    screen.blit(fon, (0, 0))
    # screen.fill(pygame.Color("black"))
    tiles_group.draw(screen)
    player_group.update()
    player_group.draw(screen)
    # board.render(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
