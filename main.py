import os
import sys
import time
import pygame
from math import sin, cos, pi, radians, degrees


pygame.init()
count = 10
size = WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode(size)
fullnameusic = os.path.join('music', 'mizuna-steps5-by-inium_effectoid.ogg.mp3')
pygame.mixer.music.load(fullnameusic)
pygame.mixer.music.play()
pygame.display.set_caption('Танки')
font = pygame.font.Font(None, 30)
# 1. для примера. Эта переменная должна будет отвечать как за действие, так и за вставленный текст в инструкции

# 2. Первое мое предложение - забиндить выстрел для человека на втором танке, который будет управлять стрелочками, на клави шу Ctrl
# 1. 2. PS Ростислав
bind_dict = {'q': 'q', 'w': 'w', 'e': 'e', 'r': 'r', 't': 't',
             'y': 'y', 'u': 'u', 'i': 'i', 'o': 'o', 'p': 'p', 
             'a': 'a', 's': 's', 'd': 'd', 'f': 'f', 'g': 'g', 
             'h': 'h', 'j': 'j', 'k': 'k', 'l': 'l', 'z': 'z', 
             'x': 'x', 'c': 'c', 'v': 'v', 'b': 'b', 'n': 'n', 
             'm': 'm', '1': '1', '2': '2', '3': '3', '4': '4', 
             '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', 
             '0': '0', 'up': 'UP', 'down': 'DOWN', 'left': 'LEFT',
             'right': 'RIGHT', 'space': 'SPACE', 'left ctrl': 'LCTRL',
             'right ctrl': 'RCTRL', 'left alt': 'LALT', 'right alt': 'RALT',
             'left shift': 'LSHIFT', 'right shift': 'RSHIFT', 'tab': 'TAB'}

first_up_down_left_right_fire_key = ['w', 's', 'a', 'd', 'e']
second_up_down_left_right_fire_key = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'LCTRL']  # Стрелочки

FPS = 60
running = True

pause = False


class Button:
    def __init__(self, space, x, y, sizex, sizey, func=None, firstkey=None):
        self.sizex = sizex
        self.sizey = sizey
        self.coords = (x, y)
        self.func = func
        self.space = space
        self.key = firstkey
        self.count = get_count()

    def act(self):
        if self.coords[0] <= pygame.mouse.get_pos()[0] <= self.coords[0] + self.sizex and \
                self.coords[1] <= \
                pygame.mouse.get_pos()[1] <= self.coords[1] + self.sizey:
            pygame.draw.rect(screen, (20, 20, 20),
                             (self.coords[0] + 3, self.coords[1] + 3, self.sizex - 6, self.sizey - 6), 5)
            pygame.display.flip()

            time.sleep(0.25)
            if self.func != None and type(self.func) != str:
                return self.func
            elif type(self.func) == str:
                if self.func in 'changebutt1' + 'changebutt2':
                    clicked = False
                    while not clicked:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and pygame.key.name(event.key).capitalize() \
                                    not in second_up_down_left_right_fire_key + first_up_down_left_right_fire_key:
                                key = pygame.key.name(event.key)
                                clicked = True
                    if self.func == 'changebutt1':
                        first_up_down_left_right_fire_key[first_up_down_left_right_fire_key.index(self.key)] = bind_dict[key]
                    if self.func == 'changebutt2':
                        second_up_down_left_right_fire_key[second_up_down_left_right_fire_key.index(self.key)] = bind_dict[key]
                    self.key = key
                if self.func in 'changeloud+' + 'changeloud-':
                    change_loud(self.func)
                if self.func == 'quit':
                    return self.func
                if self.func == 'start':
                    return 'start'
        else:
            return None

    def draw(self):
        pygame.draw.rect(self.space, (80, 80, 80), (self.coords[0], self.coords[1], self.sizex, self.sizey))
        pygame.draw.rect(self.space, (50, 50, 50), (self.coords[0], self.coords[1], self.sizex, self.sizey), 3)
        if self.coords[0] <= pygame.mouse.get_pos()[0] <= self.coords[0] + self.sizex and self.coords[1] <= \
                pygame.mouse.get_pos()[1] <= self.coords[1] + self.sizey:
            pygame.draw.rect(screen, (120, 120, 120), (self.coords[0], self.coords[1], self.sizex, self.sizey), 3)


def get_count():
    global count
    return count


def change_loud(func):
    global count
    if func == 'changeloud+':
        if count < 10:
            count += 1
            pygame.display.flip()
    elif func == 'changeloud-':
        if count > 0:
            count -= 1
            pygame.display.flip()
    pygame.mixer.music.set_volume(count / 10)


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
    global pause
    pause = False
    intro_text = ["Начать игру",
                  "Правила игры",
                  "Настройки",
                  "Информация"]
    funcs = ['start', rule_screen, set_screen, info_screen]
    Buttons = []
    text = []
    x = (WIDTH // 2) - 150
    y = 50
    buttwidth, buttheight = [300, 50]
    for line in intro_text:
        Buttons.append(Button(screen, x, y, buttwidth, buttheight, func=funcs[intro_text.index(line)]))
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = y + buttheight / 2 - font.size(line)[1] / 2
        intro_rect.x = x + buttwidth / 2 - font.size(line)[0] / 2
        text.append([string_rendered, intro_rect])
        y += 100
    while True:
        screen.fill((100, 100, 100))
        for bn in Buttons:
            bn.draw()
        for tt in text:
            screen.blit(tt[0], tt[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                for bn in Buttons:
                    answ = bn.act()
                    if answ != None:
                        if type(answ) != str:

                            answ()
                            return
                        else:
                            return

        pygame.display.flip()
        clock.tick(FPS)


def info_screen():
    screen.fill((100, 100, 100))

    info_text = ["Комманда работяг",
                 "Михаил Пивоваров 10-Б",
                 "Войцев Ростислав 10-Б",
                 "Никита Терехов 10-Б"]
    button = Button(screen, 0, 0, 90, 50, func=start_screen)
    while True:
        screen.fill((100, 100, 100))
        x, y = [75, 225 - font.size("К")[1] * 2 - 50]

        string_rendered = font.render('Назад', 1, pygame.Color('white'))
        butt_rect = string_rendered.get_rect()

        butt_rect.top = 50 / 2 - font.size('Назад')[1] / 2
        butt_rect.x = 90 / 2 - font.size('Назад')[0] / 2
        button.draw()
        screen.blit(string_rendered, butt_rect)

        for line in info_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            rule_rect = string_rendered.get_rect()
            rule_rect.x = WIDTH / 2 - font.size(line)[0] / 2

            rule_rect.top = y
            screen.blit(string_rendered, rule_rect)
            y += 50
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                answ = button.act()
                if answ != None:
                    answ()
                    return

        pygame.display.flip()
        clock.tick(FPS)


def set_screen():
    global count, pause
    set_text = ["Настройки",
                "Громкость",
                "<", ">",
                "Первый танк клавиши",
                "Второй танк клавиши"]
    while True:
        Buttons = []
        Texts = []
        Buttons.append(Button(screen, 0, 0, 90, 50, func=start_screen))
        x, y = [75, -60]
        string_rendered = font.render('Назад', 1, pygame.Color('white'))
        butt_rect = string_rendered.get_rect()
        butt_rect.top = 50 / 2 - font.size('Назад')[1] / 2
        butt_rect.x = 90 / 2 - font.size('Назад')[0] / 2
        Texts.append([string_rendered, butt_rect])
        for line in set_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            rule_rect = string_rendered.get_rect()
            if line != '<' and line != '>' and line != 'Первый танк клавиши' and line != 'Второй танк клавиши':
                rule_rect.x = WIDTH / 2 - font.size(line)[0] / 2
                y += 70
                Texts.append([string_rendered, rule_rect])

            elif line == 'Второй танк клавиши':
                rule_rect.x = WIDTH / 2 - font.size(line)[0] / 2
                y += 70
                x_butt_chg2 = 400 - (4 * 45)
                Texts.append([string_rendered, rule_rect])
                for butt in second_up_down_left_right_fire_key:
                    butt_rendered21 = font.render(butt, 1, pygame.Color('white'))
                    butt_rect21 = string_rendered.get_rect()
                    butt_rect21.x = x_butt_chg2
                    butt_rect21.top = y + 100
                    Buttons.append(Button(screen, x_butt_chg2 - 5, y + 100 - 5, 55 + 10, 20 + 10, func='changebutt2',
                                          firstkey=butt))
                    x_butt_chg2 += 25 + 55
                    Texts.append([butt_rendered21, butt_rect21])

                y += 70

            elif line == '<':
                y += 35
                rule_rect.x = WIDTH / 2 - font.size('Громкость')[0] / 2
                buttx1 = rule_rect.x
                butty1 = y
                Buttons.append(Button(screen, buttx1 - 5, butty1 - 5, font.size('<')[0] + 10, font.size('<')[1] + 10,
                                      func='changeloud-'))
                Texts.append([string_rendered, rule_rect])

            elif line == '>':
                rule_rect.x = WIDTH / 2 + font.size('Громкость')[0] / 2 - font.size('>')[0]
                butty2 = butty1
                buttx2 = rule_rect.x
                Buttons.append(Button(screen, buttx2 - 5, butty2 - 5, font.size('<')[0] + 10, font.size('<')[1] + 10,
                                      func='changeloud+'))
                Texts.append([string_rendered, rule_rect])
            elif line == 'Первый танк клавиши':
                rule_rect.x = WIDTH / 2 - font.size(line)[0] / 2
                rule_rect.top = y

                x_butt_chg1 = 400 - (4 * 45)
                Texts.append([string_rendered, rule_rect])

                for butt in first_up_down_left_right_fire_key:
                    butt_rendered11 = font.render(butt, 1, pygame.Color('white'))
                    butt_rect11 = string_rendered.get_rect()
                    butt_rect11.x = x_butt_chg1
                    butt_rect11.top = y + 100
                    Buttons.append(Button(screen, x_butt_chg1 - 5, y + 100 - 5, 55 + 10, 20 + 10, func='changebutt1',
                                          firstkey=butt))
                    x_butt_chg1 += 25 + 55
                    Texts.append([butt_rendered11, butt_rect11])

                y += 70

            rule_rect.top = y
        screen.fill((100, 100, 100))

        for bn in Buttons:
            bn.draw()
        for tt in Texts:
            screen.blit(tt[0], tt[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bt in Buttons:
                    answ = bt.act()
                    if answ != None:
                        if type(answ) != str and pause:
                            pause_window()
                            return
                        elif type(answ) != str and not pause:
                            start_screen()

                            return
                        else:
                            bt.act()

        string_rendered = font.render(str(count), 1, pygame.Color('white'))
        butt_rect = string_rendered.get_rect()
        butt_rect.x = 400 - font.size(str(count))[0] / 2
        butt_rect.top = butty2
        screen.blit(string_rendered, butt_rect)
        pygame.display.flip()

        clock.tick(FPS)


def rule_screen():
    rule_text = ["Правила игры",
                 "Первый танк",
                 f"Перемещается при зажатии клавиш {', '.join(first_up_down_left_right_fire_key[:-1])}.",
                 f"Стрельба производится по нажатии кнопки {first_up_down_left_right_fire_key[-1]}, после чего происходит",
                 "перезарядка длительностью в 4 секунды",
                 "Второй танк",
                 f"Перемещается при зажатии клавиш {', '.join(second_up_down_left_right_fire_key[:-1])}.",
                 f"Стрельба производится по нажатии кнопки {second_up_down_left_right_fire_key[-1]}, после чего происходит",
                 "перезарядка длительностью в 4 секунды"]
    x, y = [75, 10]
    Buttons = []
    Texts = []
    coord = [0, 0]

    string_rendered = font.render('Назад', 1, pygame.Color('white'))
    butt_rect = string_rendered.get_rect()
    Buttons.append(Button(screen, coord[0], coord[1], 90, 50, func=start_screen))

    butt_rect.top = 50 / 2 - font.size('Назад')[1] / 2
    butt_rect.x = 90 / 2 - font.size('Назад')[0] / 2
    Texts.append([string_rendered, butt_rect])

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
        Texts.append([string_rendered, rule_rect])
        y += 50

    while True:
        screen.fill((100, 100, 100))
        for bn in Buttons:
            bn.draw()
        for tt in Texts:
            screen.blit(tt[0], tt[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if coord[0] <= pygame.mouse.get_pos()[0] <= coord[0] + 90 and coord[1] <= \
                        pygame.mouse.get_pos()[1] <= coord[1] + 50:

                    for bn in Buttons:
                        answ = bn.act()
                        if answ != None:
                            answ()
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
    'box': load_image('box.png'),
    'wall': load_image('wall.png'),
    'empty': load_image('grass.png'),
    'destroyedgrass': load_image('destroyedgrass.png')
}

first_player_image = load_image('tank.png')
second_player_image = load_image('tank2.png')
shell_image = load_image('shell2.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.type = tile_type

    def destroy(self):
        if self.type == 'box':
            self.image = tile_images['destroyedgrass']
            self.type = 'destroyedgrass'
            box_group.remove(self)


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
box_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
shells_group = pygame.sprite.Group()


def generate_level(level):
    first_player, second_player, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                box = Tile('box', x, y)
                box_group.add(box)
            elif level[y][x] == '%':
                wall = Tile('wall', x, y)
                wall_group.add(wall)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                first_player = Player(x, y, 1)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                second_player = Player(x, y, 2)
    # вернем игрока, а также размер поля в клетках            
    return first_player, second_player, x, y


def check_tile(player):
    if pygame.sprite.spritecollide(player, box_group, False, pygame.sprite.collide_mask) or \
            pygame.sprite.spritecollide(player, wall_group, False, pygame.sprite.collide_mask):
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
        for tile in pygame.sprite.spritecollide(self, box_group, False, pygame.sprite.collide_mask):
            tile.destroy()
            self.kill()
        for tile in pygame.sprite.spritecollide(self, wall_group, False, pygame.sprite.collide_mask):
            self.kill()
        self.rect.centerx += round(self.speed * cos(self.angle))
        self.rect.centery -= round(self.speed * sin(self.angle))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player):
        super().__init__(player_group, all_sprites)

        self.stuck = False
        self.rotating = False
        self.moving = False

        if player == 1:
            self.original_image = first_player_image
            self.image = first_player_image.copy()
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
            self.angle = radians(0)
        elif player == 2:
            self.original_image = second_player_image
            self.image = second_player_image.copy()
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
            self.angle = radians(0)
            self.rotate(180)

        self.speed = 1
        self.rotating_angle = 1

        self.real_x = self.rect.centerx
        self.real_y = self.rect.centery
        self.new_real_x = self.real_x
        self.new_real_y = self.real_y

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.moving:
            self.new_real_x += self.speed * cos(self.angle)
            self.new_real_y -= self.speed * sin(self.angle)
            self.rect.centerx = round(self.new_real_x)
            self.rect.centery = round(self.new_real_y)

            if check_tile(self) is False:
                self.rect.centerx = round(self.real_x)
                self.rect.centery = round(self.real_y)
                self.new_real_x = self.real_x
                self.new_real_y = self.real_y
                self.stuck = True
            else:
                self.real_x = self.new_real_x
                self.real_y = self.new_real_y
                self.stuck = False

        if self.rotating:
            self.rotate(self.rotating_angle)

    def rotate(self, angle):
        if not self.stuck:
            self.angle += radians(angle)
            self.image = pygame.transform.rotate(self.original_image, degrees(self.angle))  # поворачиваем исходное изображение
            self.rect = self.image.get_rect(center=self.rect.center)  # устанавливаем центр изображения как точку поворота
            self.mask = pygame.mask.from_surface(self.image)


def pause_window():
    global running, pause
    intro_text = ["Пауза",
                  "Продолжить игру",
                  "Настройки",
                  "Главное меню",
                  "Выйти"]

    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))

    x = (WIDTH // 2) - 150
    funcs = ['start', set_screen, start_screen, 'quit']
    y = 50
    Buttons = []
    Texts = []
    pause = True
    buttwidth, buttheight = [300, 50]
    for line in intro_text:
        if intro_text.index(line) > 0:
            Buttons.append(Button(screen, x, y, buttwidth, buttheight, func=funcs[intro_text.index(line) - 1]))
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = y + buttheight / 2 - font.size(line)[1] / 2
        intro_rect.x = x + buttwidth / 2 - font.size(line)[0] / 2
        Texts.append([string_rendered, intro_rect])
        y += 70

    while True:
        screen.fill((100, 100, 100))
        for bn in Buttons:
            bn.draw()
        for tt in Texts:
            screen.blit(tt[0], tt[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for bn in Buttons:
                    answ = bn.act()
                    if answ != None:
                        if answ == 'start':
                            return
                        if answ == 'quit':
                            running = False
                            return
                        else:
                            pause = True
                            answ()
                            return

        pygame.display.flip()
        clock.tick(FPS)


level = load_level('map2.txt')

first_player, second_player, level_x, level_y = generate_level(level)

size = WIDTH, HEIGHT = len(level[0]) * tile_width, len(level) * tile_height
screen = pygame.display.set_mode(size)

running = True

start_screen()

rotating = False
moving = False
shell_flying = False

clock = pygame.time.Clock()
FPS = 300
coordbutt = [50, 50]
pause_button = Button(screen, 0, 0, 50, 50, func=pause_window)

while running:
    delta_time = clock.tick(FPS) / 1000
    pause_button.draw()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            answ = pause_button.act()
            if answ != None:
                answ()
            break
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Движение и стрельба первого танка

            if event.key == getattr(pygame, 'K_' + first_up_down_left_right_fire_key[0]):
                if first_player.speed < 0:
                    first_player.speed *= -1
                first_player.moving = True
            if event.key == getattr(pygame, 'K_' + first_up_down_left_right_fire_key[1]):
                first_player.moving = True
                if first_player.speed > 0:
                    first_player.speed *= -1
            if event.key == getattr(pygame, 'K_' + first_up_down_left_right_fire_key[2]):
                if first_player.rotating_angle < 0:
                    first_player.rotating_angle *= -1
                first_player.rotating = True
            if event.key == getattr(pygame, 'K_' + first_up_down_left_right_fire_key[3]):
                if first_player.rotating_angle > 0:
                    first_player.rotating_angle *= -1
                first_player.rotating = True
            if event.key == getattr(pygame, 'K_' + first_up_down_left_right_fire_key[4]):
                shell = TankShell(first_player.rect.centerx, first_player.rect.centery, first_player.angle)
                shell_flying = True

            # Движение и стрельба второго танка

            if event.type == pygame.KEYDOWN:
                if event.key == getattr(pygame, 'K_' + second_up_down_left_right_fire_key[0]):
                    if second_player.speed < 0:
                        second_player.speed *= -1
                    second_player.moving = True
                if event.key == getattr(pygame, 'K_' + second_up_down_left_right_fire_key[1]):
                    second_player.moving = True
                    if second_player.speed > 0:
                        second_player.speed *= -1
                if event.key == getattr(pygame, 'K_' + second_up_down_left_right_fire_key[2]):
                    if second_player.rotating_angle < 0:
                        second_player.rotating_angle *= -1
                    second_player.rotating = True
                if event.key == getattr(pygame, 'K_' + second_up_down_left_right_fire_key[3]):
                    if second_player.rotating_angle > 0:
                        second_player.rotating_angle *= -1
                    second_player.rotating = True
                if event.key == getattr(pygame, 'K_' + second_up_down_left_right_fire_key[4]):
                    shell = TankShell(second_player.rect.centerx, second_player.rect.centery, second_player.angle)
                    shell_flying = True

        if event.type == pygame.KEYUP:

            # Остановка первого танка

            keys = pygame.key.get_pressed()
            if event.key == getattr(pygame, 'K_' + first_up_down_left_right_fire_key[2]):
                if not keys[getattr(pygame, 'K_' + first_up_down_left_right_fire_key[3])]:
                    first_player.rotating = False
                elif first_player.rotating_angle > 0:
                    first_player.rotating_angle *= -1
            if event.key == getattr(pygame, 'K_' + first_up_down_left_right_fire_key[3]):
                if not keys[getattr(pygame, 'K_' + first_up_down_left_right_fire_key[2])]:
                    first_player.rotating = False
                elif first_player.rotating_angle < 0:
                    first_player.rotating_angle *= -1
            if event.key == getattr(pygame, 'K_' + first_up_down_left_right_fire_key[0]):
                first_player.moving = False
            if event.key == getattr(pygame, 'K_' + first_up_down_left_right_fire_key[1]):
                first_player.moving = False

            # Остановка второго танка

            if event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                if event.key == getattr(pygame, 'K_' + second_up_down_left_right_fire_key[2]):
                    if not keys[getattr(pygame, 'K_' + second_up_down_left_right_fire_key[3])]:
                        second_player.rotating = False
                    elif second_player.rotating_angle > 0:
                        second_player.rotating_angle *= -1
                if event.key == getattr(pygame, 'K_' + second_up_down_left_right_fire_key[3]):
                    if not keys[getattr(pygame, 'K_' + second_up_down_left_right_fire_key[2])]:
                        second_player.rotating = False
                    elif second_player.rotating_angle < 0:
                        second_player.rotating_angle *= -1
                if event.key == getattr(pygame, 'K_' + second_up_down_left_right_fire_key[0]):
                    second_player.moving = False
                if event.key == getattr(pygame, 'K_' + second_up_down_left_right_fire_key[1]):
                    second_player.moving = False

    all_sprites.update()

    screen.fill(pygame.Color('black'))
    tiles_group.draw(screen)
    shells_group.draw(screen)
    player_group.draw(screen)

    pygame.draw.rect(screen, (80, 80, 80), (0, 0, 50, 50))
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, 50, 50), 3)
    string_rendered = font.render('| |', 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 25 - font.size('| |')[1] / 2
    intro_rect.x = 25 - font.size('| |')[0] / 2
    if 0 <= pygame.mouse.get_pos()[0] <= 50 and 0 <= pygame.mouse.get_pos()[1] <= 50:
        pygame.draw.rect(screen, (120, 120, 120), (0, 0, 50, 50), 3)
    screen.blit(string_rendered, intro_rect)

    pygame.display.flip()

    clock.tick(FPS)
