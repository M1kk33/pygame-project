import os
import sys
import pygame
from math import sin, cos, pi, radians, degrees


pygame.init()
size = WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Перемещение героя')


FPS = 60


def load_image(name, colorkey=None):
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
    pygame.quit()
    sys.exit()


clock = pygame.time.Clock()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


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
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}

player_image = load_image('tank.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках            
    return new_player, x, y


def check_tile(player, level, key):
    if key == pygame.K_w:
        tile_x = player.rect.x // tile_width
        tile_y = (player.rect.y - tile_height) // tile_height
    elif key == pygame.K_s:
        tile_x = player.rect.x // tile_width
        tile_y = (player.rect.y + tile_height) // tile_height
    elif key == pygame.K_a:
        tile_x = (player.rect.x - tile_width) // tile_width
        tile_y = player.rect.y // tile_height
    elif key == pygame.K_d:
        tile_x = (player.rect.x + tile_width) // tile_width
        tile_y = player.rect.y // tile_height

    if 0 <= tile_x < len(level[0]) and 0 <= tile_y < len(level):
        return level[tile_y][tile_x]

    return None 


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.original_image = player_image
        self.image = player_image.copy()
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.angle = radians(0)
        self.speed = 100
        self.real_x = self.rect.x  # инициализация real_x
        self.real_y = self.rect.y  # инициализация real_y
        
    def move(self, delta_time, key):
        # tile_above_player = check_tile(player, level, key)
        # if tile_above_player is not None and tile_above_player != '#':
            # dx = cos(radians(self.angle)) * speed
            # dy = sin(radians(self.angle)) * speed
            # self.rect.x += dx
            # self.rect.y += dy
        path = self.speed * delta_time
        self.real_x += path * cos(self.angle)
        self.real_y -= path * sin(self.angle)
        self.rect.x = round(self.real_x)
        self.rect.y = round(self.real_y)

    def rotate(self, angle):
        self.angle += radians(angle)
        self.image = pygame.transform.rotate(self.original_image, degrees(self.angle))  # поворачиваем исходное изображение
        self.rect = self.image.get_rect(center=self.rect.center)  # устанавливаем центр изображения как точку поворота


level = load_level('field.txt')

player, level_x, level_y = generate_level(level)

size = WIDTH, HEIGHT = len(level[0]) * tile_width, len(level) * tile_height
screen = pygame.display.set_mode(size)

running = True

start_screen()

turn_plus = False
turn_minus = False
moving = False

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                moving = True
                player.speed = 100
            if event.key == pygame.K_s:
                moving = True
                player.speed = -100
            if event.key == pygame.K_a:
                turn_plus = True
            if event.key == pygame.K_d:
                turn_minus = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                turn_plus = False
            if event.key == pygame.K_d:
                turn_minus = False
            if event.key == pygame.K_w:
                moving = False
            if event.key == pygame.K_s:
                moving = False

    if turn_plus:
        player.rotate(1)
    if turn_minus:
        player.rotate(-1) 
    if moving:
        player.move(clock.get_time() / 1000, pygame.K_w)


    all_sprites.update()

    screen.fill(pygame.Color('black'))
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)