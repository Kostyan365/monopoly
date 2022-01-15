import pygame
import os
import sys
import ctypes
import random
list_sound=['brosok-igralnyih-kostey','brosok-igralnyih-kostey-25740','igralnaya-kost-upala','katyatsya-po-stolu',
            'kubiki-razletelis','odin-kubik-brosili-na-stol','zvuk-brosaniya-igralnyih-kostey-2-25771']
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
FPS = 50
# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_width = 70
tile_height = 70


def load_img(name, colorkey=None):
    """Функция для удобства загрузки изображений"""
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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


player_image = load_img('mario.png')


def terminate():
    """Функция выхода"""
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    '#': load_img('atlas.jpg'),
    '.': load_img('grass.png'),
    'q': load_img('start1.jpg'),
    'w': load_img('start2.jpg'),
    'e': load_img('start3.jpg'),
    'r': load_img('start4.jpg'),
    't': load_img('prisoner1.jpg'),
    'y': load_img('prisoner2.jpg'),
    'u': load_img('prisoner3.jpg'),
    'i': load_img('prisoner4.jpg'),

    'o': load_img('parking1.jpg'),
    'p': load_img('parking2.jpg'),
    'a': load_img('parking3.jpg'),
    's': load_img('parking4.jpg'),

    'd': load_img('arest1.jpg'),
    'f': load_img('arest2.jpg'),
    'g': load_img('arest3.jpg'),
    'h': load_img('arest4.jpg'),
    'j': load_img('shans1.jpg'),
    'k': load_img('shans2.jpg'),
    'l': load_img('shans3.jpg'),
    ';': load_img('shans4.jpg'),
    'z': load_img('kazna1.jpg'),
    'x': load_img('kazna2.jpg')
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + (width / 2 - 455), tile_height * pos_y + 100)


class Cards:
    def __init__(self, **kwargs):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image

        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                Tile('q', x, y)
                new_player = Player(x, y)
            else:
                Tile(level[y][x], x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def start_screen():
    pygame.mixer.music.load("3d20874f20174bd.mp3")
    pygame.mixer.music.play(-1)
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


start_screen()
level_map = load_level('map.map')
player, max_x, max_y = generate_level(level_map)
print(player)


def dice():

    z=random.choice(list_sound)

    s_catch = pygame.mixer.Sound(f'sound/{z}.ogg')
    s_catch.play()

class Board:
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
        print(ceil)

dice()
fon = pygame.transform.scale(load_img('fon2.jpg'), (width, height))

board = Board(13, 13)
board.set_view(width / 2 - 455, 100, 70)
running = True
while running:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
        if width / 2 - 100 <= mouse[0] <= width / 2 + 100 and height / 1.5 + 60 <= mouse[1] <= height / 1.5 + 60 + 40:
            terminate()  # Если мышь нажала на кнопку игра прекращена

    screen.blit(fon, (0, 0))

    tiles_group.draw(screen)
    board.render(screen)
    Tile('q', 11, 1)
    pygame.display.flip()

pygame.quit()
