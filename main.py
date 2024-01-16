import os
import sys
import pygame
from math import sin, cos, pi, radians, degrees


pygame.init()
size = WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode(size)
fullnameusic = os.path.join('music', 'mizuna-steps5-by-inium_effectoid.ogg.mp3')
pygame.mixer.music.load(fullnameusic)
pygame.mixer.music.play()
pygame.display.set_caption('Танки')
font = pygame.font.Font(None, 30)
# 1. для примера. Эта переменная должна будет отвечать как за действие, так и за вставленный текст в инструкции

# 2. Первое мое предложение - забиндить выстрел для человека на втором танке, который будет управлять стрелочками, на клавишу Ctrl
# 1. 2. PS Ростислав
first_up_down_left_right_fire_key = ['W', 'S', 'A', 'D', 'E']
second_up_down_left_right_fire_key = ['Up', 'Down', 'Left', 'Right', 'Ctrl']  # Стрелочки

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
                if coords[2][0] <= pygame.mouse.get_pos()[0] <= coords[2][0] + 300 and coords[2][1] <= \
                        pygame.mouse.get_pos()[1] <= coords[2][1] + 50:
                    set_screen()
                    return
                if coords[3][0] <= pygame.mouse.get_pos()[0] <= coords[3][0] + 300 and coords[3][1] <= \
                        pygame.mouse.get_pos()[1] <= coords[3][1] + 50:
                    info_screen()
                    return
        pygame.display.flip()
        clock.tick(FPS)


def info_screen():
    screen.fill((100, 100, 100))

    info_text = ["Комманда работяг",
                 "Михаил Пивоваров 10-Б",
                 "Войцев Ростислав 10-Б",
                 "Никита Терехов 10-Б"]
    x, y = [75, 225 - font.size("К")[1] * 2 - 50]
    coord = [0, 0]

    string_rendered = font.render('Назад', 1, pygame.Color('white'))
    butt_rect = string_rendered.get_rect()
    pygame.draw.rect(screen, (80, 80, 80), (coord[0], coord[1], 90, 50))
    pygame.draw.rect(screen, (50, 50, 50), (coord[0], coord[1], 90, 50), 3)

    butt_rect.top = 50 / 2 - font.size('Назад')[1] / 2
    butt_rect.x = 90 / 2 - font.size('Назад')[0] / 2
    screen.blit(string_rendered, butt_rect)

    for line in info_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        rule_rect = string_rendered.get_rect()
        rule_rect.x = WIDTH / 2 - font.size(line)[0] / 2

        rule_rect.top = y
        screen.blit(string_rendered, rule_rect)
        y += 50

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if coord[0] <= pygame.mouse.get_pos()[0] <= coord[0] + 90 and coord[1] <= \
                        pygame.mouse.get_pos()[1] <= coord[1] + 50:
                    start_screen()
                    return

        pygame.display.flip()
        clock.tick(FPS)


def set_screen():
    set_text = ["Настройки",
                "Громкость",
                "<", ">",
                "Первый танк клавиши",
                "Второй танк клавиши"]
    count = 10

    while True:
        x, y = [75, -60]  # y = -90 т.к. в дальнейшем при отрисовке первого текста y = y + 100
        coord = [0, 0]
        change_butt_coords1 = []
        change_butt_coords2 = []
        screen.fill((100, 100, 100))
        clicked = False
        string_rendered = font.render('Назад', 1, pygame.Color('white'))
        butt_rect = string_rendered.get_rect()
        pygame.draw.rect(screen, (80, 80, 80), (coord[0], coord[1], 90, 50))
        pygame.draw.rect(screen, (50, 50, 50), (coord[0], coord[1], 90, 50), 3)

        butt_rect.top = 50 / 2 - font.size('Назад')[1] / 2
        butt_rect.x = 90 / 2 - font.size('Назад')[0] / 2
        screen.blit(string_rendered, butt_rect)
        for line in set_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            rule_rect = string_rendered.get_rect()
            if line != '<' and line != '>' and line != 'Первый танк клавиши' and line != 'Второй танк клавиши':
                rule_rect.x = WIDTH / 2 - font.size(line)[0] / 2
                y += 70

            elif line == 'Второй танк клавиши':
                rule_rect.x = WIDTH / 2 - font.size(line)[0] / 2
                y += 70
                x_butt_chg2 = 400 - (4 * 45)

                for butt in second_up_down_left_right_fire_key:
                    butt_rendered21 = font.render(butt, 1, pygame.Color('white'))
                    butt_rect21 = string_rendered.get_rect()
                    butt_rect21.x = x_butt_chg2
                    butt_rect21.top = y + 100
                    change_butt_coords2.append([butt_rect21.x, butt_rect21.top])

                    pygame.draw.rect(screen, (80, 80, 80),
                                     (x_butt_chg2 - 5, y + 100 - 5, 55 + 10, 20 + 10))
                    pygame.draw.rect(screen, (50, 50, 50),
                                     (x_butt_chg2 - 5, y + 100 - 5, 55 + 10, 20 + 10),
                                     3)
                    x_butt_chg2 += 25 + 55
                    screen.blit(butt_rendered21, butt_rect21)

                y += 70

            elif line == '<':
                y += 35
                rule_rect.x = WIDTH / 2 - font.size('Громкость')[0] / 2
                buttx1 = rule_rect.x
                butty1 = y
                pygame.draw.rect(screen, (80, 80, 80),
                                 (buttx1 - 5, butty1 - 5, font.size('<')[0] + 10, font.size('<')[1] + 10))
                pygame.draw.rect(screen, (50, 50, 50),
                                 (buttx1 - 5, butty1 - 5, font.size('<')[0] + 10, font.size('<')[1] + 10), 3)

            elif line == '>':
                rule_rect.x = WIDTH / 2 + font.size('Громкость')[0] / 2 - font.size('>')[0]
                butty2 = butty1
                buttx2 = rule_rect.x
                pygame.draw.rect(screen, (80, 80, 80),
                                 (buttx2 - 5, butty2 - 5, font.size('<')[0] + 10, font.size('<')[1] + 10))
                pygame.draw.rect(screen, (50, 50, 50),
                                 (buttx2 - 5, butty2 - 5, font.size('<')[0] + 10, font.size('<')[1] + 10), 3)
            elif line == 'Первый танк клавиши':
                rule_rect.x = WIDTH / 2 - font.size(line)[0] / 2
                rule_rect.top = y

                x_butt_chg1 = 400 - (4 * 45)

                for butt in first_up_down_left_right_fire_key:
                    butt_rendered11 = font.render(butt, 1, pygame.Color('white'))
                    butt_rect11 = string_rendered.get_rect()
                    butt_rect11.x = x_butt_chg1
                    butt_rect11.top = y + 100
                    change_butt_coords1.append([butt_rect11.x, butt_rect11.top])

                    pygame.draw.rect(screen, (80, 80, 80),
                                     (x_butt_chg1 - 5, y + 100 - 5, 55 + 10, 20 + 10))
                    pygame.draw.rect(screen, (50, 50, 50),
                                     (x_butt_chg1 - 5, y + 100 - 5, 55 + 10, 20 + 10),
                                     3)  # 19 - величина будто бы самой широкой буквы, т.к.
                    # судя по рендеру размеры у букв разные
                    #   20 - просто высота той же буквы но у всех букв она вроде одинаковая
                    x_butt_chg1 += 25 + 55
                    screen.blit(butt_rendered11, butt_rect11)


                y += 70


            rule_rect.top = y

            screen.blit(string_rendered, rule_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if coord[0] <= pygame.mouse.get_pos()[0] <= coord[0] + 90 and coord[1] <= \
                        pygame.mouse.get_pos()[1] <= coord[1] + 50:
                    start_screen()
                    return
                if buttx1 <= pygame.mouse.get_pos()[0] <= buttx1 + font.size('<')[0] and butty1 <= \
                        pygame.mouse.get_pos()[1] <= butty1 + font.size('<')[
                    1] and count > 0:  # максимальная громкость - 10
                    count -= 1
                    pygame.mixer.music.set_volume(count / 10)
                if buttx2 <= pygame.mouse.get_pos()[0] <= buttx2 + font.size('>')[0] and butty2 <= \
                        pygame.mouse.get_pos()[1] <= butty2 + font.size('>')[1] and count < 10:
                    count += 1
                    pygame.mixer.music.set_volume(count / 10)
                for i in change_butt_coords1:
                    button = change_butt_coords1.index(i)
                    if i[0] <= pygame.mouse.get_pos()[0] <= i[0] + 65 and i[1] <= pygame.mouse.get_pos()[1] <= i[1] + 30:
                        while not clicked:
                            for event1 in pygame.event.get():
                                if event1.type == pygame.KEYDOWN and pygame.key.name(event1.key).upper() \
                                        not in second_up_down_left_right_fire_key + first_up_down_left_right_fire_key:
                                    key = pygame.key.name(event1.key).capitalize()
                                    first_up_down_left_right_fire_key[button] = key
                                    clicked = True
                for i in change_butt_coords2:
                    button = change_butt_coords2.index(i)
                    if i[0] <= pygame.mouse.get_pos()[0] <= i[0] + 65 and i[1] <= pygame.mouse.get_pos()[1] <= i[1] + 30:
                        while not clicked:
                            for event2 in pygame.event.get():
                                if event2.type == pygame.KEYDOWN and pygame.key.name(event2.key).upper() \
                                        not in second_up_down_left_right_fire_key + first_up_down_left_right_fire_key:
                                    key = pygame.key.name(event2.key).capitalize()
                                    second_up_down_left_right_fire_key[button] = key
                                    clicked = True

        string_rendered = font.render(str(count), 1, pygame.Color('white'))
        butt_rect = string_rendered.get_rect()
        butt_rect.x = 400 - font.size(str(count))[0] / 2
        butt_rect.top = butty2
        screen.blit(string_rendered, butt_rect)
        pygame.display.flip()

        clock.tick(FPS)


def rule_screen():
    screen.fill((100, 100, 100))
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
    coord = [0, 0]

    string_rendered = font.render('Назад', 1, pygame.Color('white'))
    butt_rect = string_rendered.get_rect()
    pygame.draw.rect(screen, (80, 80, 80), (coord[0], coord[1], 90, 50))
    pygame.draw.rect(screen, (50, 50, 50), (coord[0], coord[1], 90, 50), 3)

    butt_rect.top = 50 / 2 - font.size('Назад')[1] / 2
    butt_rect.x = 90 / 2 - font.size('Назад')[0] / 2
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
                if coord[0] <= pygame.mouse.get_pos()[0] <= coord[0] + 90 and coord[1] <= \
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

while running:
    delta_time = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Движение и стрельба первого танка

            if event.key == pygame.K_w:
                if first_player.speed < 0:
                    first_player.speed *= -1 
                first_player.moving = True
            if event.key == pygame.K_s:
                first_player.moving = True
                if first_player.speed > 0:
                    first_player.speed *= -1 
            if event.key == pygame.K_a:
                if first_player.rotating_angle < 0:
                    first_player.rotating_angle *= -1
                first_player.rotating = True
            if event.key == pygame.K_d:
                if first_player.rotating_angle > 0:
                    first_player.rotating_angle *= -1
                first_player.rotating = True
            if event.key == pygame.K_e:
                shell = TankShell(first_player.rect.centerx, first_player.rect.centery, first_player.angle)
                shell_flying = True

            # Движение и стрельба второго танка

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if second_player.speed < 0:
                        second_player.speed *= -1 
                    second_player.moving = True
                if event.key == pygame.K_DOWN:
                    second_player.moving = True
                    if second_player.speed > 0:
                        second_player.speed *= -1 
                if event.key == pygame.K_LEFT:
                    if second_player.rotating_angle < 0:
                        second_player.rotating_angle *= -1
                    second_player.rotating = True
                if event.key == pygame.K_RIGHT:
                    if second_player.rotating_angle > 0:
                        second_player.rotating_angle *= -1
                    second_player.rotating = True
                if event.key == pygame.K_RCTRL:
                    shell = TankShell(second_player.rect.centerx, second_player.rect.centery, second_player.angle)
                    shell_flying = True

        if event.type == pygame.KEYUP:

            # Остановка первого танка

            keys = pygame.key.get_pressed()
            if event.key == pygame.K_a:
                if not keys[pygame.K_d]:
                    first_player.rotating = False
                elif first_player.rotating_angle > 0:
                    first_player.rotating_angle *= -1
            if event.key == pygame.K_d:
                if not keys[pygame.K_a]:
                    first_player.rotating = False
                elif first_player.rotating_angle < 0:
                    first_player.rotating_angle *= -1
            if event.key == pygame.K_w:
                first_player.moving = False
            if event.key == pygame.K_s:
                first_player.moving = False

            # Остановка второго танка

            if event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                if event.key == pygame.K_LEFT:
                    if not keys[pygame.K_RIGHT]:
                        second_player.rotating = False
                    elif second_player.rotating_angle > 0:
                        second_player.rotating_angle *= -1
                if event.key == pygame.K_RIGHT:
                    if not keys[pygame.K_LEFT]:
                        second_player.rotating = False
                    elif second_player.rotating_angle < 0:
                        second_player.rotating_angle *= -1
                if event.key == pygame.K_UP:
                    second_player.moving = False
                if event.key == pygame.K_DOWN:
                    second_player.moving = False

    all_sprites.update()

    screen.fill(pygame.Color('black'))
    tiles_group.draw(screen)
    shells_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
