import os
import sys
import pygame
from math import sin, cos, pi, radians, degrees


pygame.init()
size = WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Танки')
font = pygame.font.Font(None, 30)
first_fire_key = 'E'  # 1. для примера. Эта переменная должна будет отвечать как за действие, так и за вставленный текст в инструкции

second_fire_key = 'Ctrl'  # 2. Первое мое предложение - забиндить выстрел для человека на втором танке, который будет управлять стрелочками, на клавишу Ctrl
# 1. 2. PS Ростислав
firs_up_down_left_right_key = ['W', 'S', 'A', 'D']
second_up_down_left_right_key = ['Up', 'Down', 'Left', 'Right']  # Стрелочки

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
    screen.fill((100, 100, 100))
    intro_text = ["Начать игру",
                  "Правила игры",
                  "Настройки",
                  "Информация"]

    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    x = (WIDTH // 2) - 150
    y = 50
    coords = [[x, i] for i in range(50, 450, 100)]
    buttsize = buttwidth, buttheight = [300, 50]
    for line in intro_text:
        """string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 400 - len(line) / 2 * 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)"""
        pygame.draw.rect(screen, (80, 80, 80), (x, y, buttwidth, buttheight))
        pygame.draw.rect(screen, (50, 50, 50), (x, y, buttwidth, buttheight), 3)
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = y + buttheight / 2 - font.size(line)[1] / 2
        intro_rect.x = x + buttwidth / 2 - font.size(line)[0] / 2
        screen.blit(string_rendered, intro_rect)
        y += 100

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if coords[0][0] <= pygame.mouse.get_pos()[0] <= coords[0][0] + 300 and coords[0][1] <= \
                        pygame.mouse.get_pos()[1] <= coords[0][1] + 50:
                    return
                if coords[1][0] <= pygame.mouse.get_pos()[0] <= coords[1][0] + 300 and coords[1][1] <= \
                        pygame.mouse.get_pos()[1] <= coords[1][1] + 50:
                    rule_screen()
                    return
        pygame.display.flip()
        clock.tick(FPS)


def rule_screen():
    screen.fill((100, 100, 100))
    rule_text = ["Правила игры",
                 "Первый танк",
                 f"Перемещается при зажатии клавиш {', '.join(firs_up_down_left_right_key)}.",
                 f"Стрельба производится по нажатии кнопки {first_fire_key}, после чего происходит",
                 "перезарядка длительностью в 4 секунды",
                 "Второй танк",
                 f"Перемещается при зажатии клавиш {', '.join(second_up_down_left_right_key)}.",
                 f"Стрельба производится по нажатии кнопки {second_fire_key}, после чего происходит",
                 "перезарядка длительностью в 4 секунды"]

    start_x, start_y = [75, 75]
    x, y = [75, 10]
    coord = [0, 0]

    string_rendered = font.render('Назад', 1, pygame.Color('white'))
    butt_rect = string_rendered.get_rect()
    pygame.draw.rect(screen, (80, 80, 80), (coord[0], coord[1], 75, 50))
    pygame.draw.rect(screen, (50, 50, 50), (coord[0], coord[1], 75, 50), 3)

    butt_rect.top = 25 - font.size('Назад')[1] / 2
    butt_rect.x = 75 / 2 - font.size('Назад')[0] / 2
    screen.blit(string_rendered, butt_rect)

    for line in rule_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        rule_rect = string_rendered.get_rect()
        if line == 'Правила игры' or line == 'Первый танк' or line == 'Второй танк':
            rule_rect.x = WIDTH / 2 - font.size(line)[0] / 2
        elif 'перезарядка' in line:
            rule_rect.x = 10
        else:
            rule_rect.x = 25

        rule_rect.top = y
        screen.blit(string_rendered, rule_rect)
        y += 50

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if coord[0] <= pygame.mouse.get_pos()[0] <= coord[0] + 75 and coord[1] <= \
                        pygame.mouse.get_pos()[1] <= coord[1] + 50:
                    start_screen()
                    return

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
shell_image = load_image('shell2.png')

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
wall_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
shells_group = pygame.sprite.Group()

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                wall = Tile('wall', x, y)
                wall_group.add(wall)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках            
    return new_player, x, y


def check_tile(player, key, real_x, real_y):
    if pygame.sprite.spritecollide(player, wall_group, False, pygame.sprite.collide_mask):
        return False
    return True


class TankShell(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, angle):
        super().__init__(shells_group, all_sprites)
        self.original_image = shell_image
        self.image = shell_image.copy()
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.angle = angle
        self.speed = 4.6

        self.image = pygame.transform.rotate(self.original_image, degrees(self.angle - pi / 2))
        self.rect = self.image.get_rect(center=self.rect.center)  # устанавливаем центр изображения как точку поворота
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.centerx += round(self.speed * cos(self.angle))
        self.rect.centery -= round(self.speed * sin(self.angle))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.original_image = player_image
        self.image = player_image.copy()
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.angle = radians(0)
        self.speed = 200

        self.real_x = self.rect.centerx
        self.real_y = self.rect.centery
        self.new_real_x = self.real_x
        self.new_real_y = self.real_y
        self.stuck = False

        self.mask = pygame.mask.from_surface(self.image)

    def move(self, delta_time, key):
        path = self.speed * delta_time
        self.new_real_x += path * cos(self.angle)
        self.new_real_y -= path * sin(self.angle)
        self.rect.centerx = round(self.new_real_x)
        self.rect.centery = round(self.new_real_y)

        if check_tile(self, key, self.real_x, self.real_y) is False:
            self.rect.centerx = round(self.real_x)
            self.rect.centery = round(self.real_y)
            self.new_real_x = self.real_x
            self.new_real_y = self.real_y
            self.stuck = True
        else:
            self.real_x = self.new_real_x
            self.real_y = self.new_real_y
            self.stuck = False

    def rotate(self, angle):
        if not self.stuck:
            self.angle += radians(angle)
            self.image = pygame.transform.rotate(self.original_image, degrees(self.angle))  # поворачиваем исходное изображение
            self.rect = self.image.get_rect(center=self.rect.center)  # устанавливаем центр изображения как точку поворота
            self.mask = pygame.mask.from_surface(self.image)


level = load_level('map2.txt')

player, level_x, level_y = generate_level(level)

size = WIDTH, HEIGHT = len(level[0]) * tile_width, len(level) * tile_height
screen = pygame.display.set_mode(size)

running = True

start_screen()

turn_plus = False
turn_minus = False
moving = False
shell_flying = False

clock = pygame.time.Clock()
FPS = 300

while running:
    delta_time = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if player.speed < 0:
                    player.speed *= -1 
                moving = True
            if event.key == pygame.K_s:
                moving = True
                if player.speed > 0:
                    player.speed *= -1 
            if event.key == pygame.K_a:
                turn_plus = True
            if event.key == pygame.K_d:
                turn_minus = True
            if event.key == pygame.K_e:
                shell = TankShell(player.rect.centerx, player.rect.centery, player.angle)
                shell_flying = True
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
        player.move(delta_time, pygame.K_w)

    all_sprites.update()

    screen.fill(pygame.Color('black'))
    tiles_group.draw(screen)
    shells_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
