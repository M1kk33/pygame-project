import os
import sys
import time
import pygame
from math import sin, cos, pi, radians, degrees
import sqlite3

start_folder = os.getcwd()
if not (os.path.exists(os.getcwd() + '\ '.strip() + os.path.join('database', 'games.db'))):
    if not (os.path.exists(os.getcwd() + '\ '.strip() + 'database')):
        os.mkdir("database")
    os.chdir('database')
    conn = sqlite3.connect('games.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Games(
    id INTEGER,
    wins_first_player INTEGER,
    wins_second_player INTEGER,
    game_time TEXT)''')
    conn.commit()
    conn.close()
    os.chdir(start_folder)
start_time, finish_time = time.gmtime(), time.gmtime()
pygame.init()
size = WIDTH, HEIGHT = 800, 450
sound_level = 10
screen = pygame.display.set_mode(size)
fullnameusic = os.path.join('music', 'mizuna-steps5-by-inium_effectoid.ogg.mp3')
path = os.getcwd() + '\ '.strip() + fullnameusic
pygame.mixer.music.load(path)
pygame.mixer.music.play()
pygame.display.set_caption('Танки')
font = pygame.font.Font('data\joystix monospace.ttf', 16)
wins = {'first': 0, 'second': 0}

# 1. для примера. Эта переменная должна будет отвечать как за действие, так и за вставленный текст в инструкции

# 2. Первое мое предложение - забиндить выстрел для человека на втором танке, который будет управлять стрелочками, на клави шу Ctrl
# 1. 2. PS Ростислав
bind_dict = {'Q': 'q', 'W': 'w', 'E': 'e', 'R': 'r', 'T': 't',
             'Y': 'y', 'U': 'u', 'I': 'i', 'O': 'o', 'P': 'p',
             'A': 'a', 'S': 's', 'D': 'd', 'F': 'f', 'G': 'g',
             'H': 'h', 'J': 'j', 'K': 'k', 'L': 'l', 'Z': 'z',
             'X': 'x', 'C': 'c', 'V': 'v', 'B': 'b', 'N': 'n',
             'M': 'm', '1': '1', '2': '2', '3': '3', '4': '4',
             '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
             '0': '0', '1^': 'KP1', '2^': 'KP2', '3^': 'KP3', '4^': 'KP4',
             '5^': 'KP5', '6^': 'KP6', '7^': 'KP7', '8^': 'KP8', '9^': 'KP9',
             '0^': 'KP0', 'Up': 'UP', 'Down': 'DOWN', 'Left': 'LEFT',
             'Right': 'RIGHT', 'Space': 'SPACE', 'Lctrl': 'LCTRL',
             'Rctrl': 'RCTRL', 'Lalt': 'LALT', 'Ralt': 'RALT',
             'Lshift': 'LSHIFT', 'Rshift': 'RSHIFT', 'Tab': 'TAB'}

first_up_down_left_right_fire_key = ['W', 'S', 'A', 'D', 'E']
second_up_down_left_right_fire_key = ['Up', 'Down', 'Left', 'Right', 'Rctrl']  # Стрелочки
maps = ['field.txt', 'map2.txt']
FPS = 60
running = True
countmap = 0
pause = False


class GameSettings:
    def __init__(self, sound_level, first_up_down_left_right_fire_key, second_up_down_left_right_fire_key):
        self.sound_level = sound_level
        self.first_up_down_left_right_fire_key = first_up_down_left_right_fire_key
        self.second_up_down_left_right_fire_key = second_up_down_left_right_fire_key

    def change_loud(self, func):
        if func == 'changeloud+':
            if self.sound_level < 10:
                self.sound_level += 1
        elif func == 'changeloud-':
            if self.sound_level > 0:
                self.sound_level -= 1
        pygame.display.flip()
        pygame.mixer.music.set_volume(self.sound_level / 10)


settings = GameSettings(sound_level, first_up_down_left_right_fire_key, second_up_down_left_right_fire_key)


def win_screen(player):
    global running, finish_time, start_time, countmap
    pygame.event.set_blocked(pygame.KEYDOWN)
    pygame.event.set_blocked(pygame.KEYUP)
    if player == "Первый игрок":
        wins['first'] += 1
    if player == "Второй игрок":
        wins['second'] += 1
    if countmap + 1 < len(maps):
        win_text = f"{player} выиграл!"

        if 'Ничья' in player:
            win_text = f"Ничья!"
        screen.fill((100, 100, 100))
        string_rendered = font.render(win_text, 1, pygame.Color('white'))
        win_rect = string_rendered.get_rect()
        win_rect.top = 225 - font.size(win_text)[1] / 2
        win_rect.x = 400 - font.size(win_text)[0] / 2
        screen.blit(string_rendered, win_rect)
        pygame.display.flip()
        time.sleep(0.8)
        countmap += 1
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.event.set_allowed(pygame.KEYUP)
        running = True
        start(load_level(maps[countmap]))
        return
    else:
        finish_time = time.gmtime()
        dbtime = f"{str(finish_time.tm_hour - start_time.tm_hour).rjust(2, '0')}:{str(finish_time.tm_min - start_time.tm_min).rjust(2, '0')}:{str(finish_time.tm_sec - start_time.tm_sec).rjust(2, '0')}"
        if wins['first'] > wins['second']:
            win_text = ['Первый игрок выиграл', "Счёт", f"Первый игрок: {wins['first']}",
                        f"Второй игрок: {wins['second']}", 'Главное меню', 'Выйти']
        elif wins['first'] < wins['second']:
            win_text = ['Второй игрок выиграл', "Счёт", f"Первый игрок: {wins['first']}",
                        f"Второй игрок: {wins['second']}", 'Главное меню', 'Выйти']
        else:
            win_text = ['Ничья', "Счёт", f"Первый игрок: {wins['first']}",
                        f"Второй игрок: {wins['second']}", 'Главное меню', 'Выйти']
        os.chdir('database')
        conn = sqlite3.connect('games.db')
        cur = conn.cursor()
        count = cur.execute('''SELECT COUNT(id) FROM Games''').fetchone()
        cur.execute('''INSERT INTO Games (id, wins_first_player, wins_second_player, game_time) VALUES (?, ?, ?, ?)''',
                    (count[0] + 1, wins['first'], wins['second'], dbtime))
        conn.commit()
        conn.close()
        os.chdir(start_folder)
        while True:
            pygame.event.set_allowed(pygame.KEYDOWN)
            pygame.event.set_allowed(pygame.KEYUP)
            screen.fill((100, 100, 100))
            funcs = [start_screen, 'quit']
            Text = []
            Buttons = []
            buttsizex = 180
            buttsizey = 30
            first_coords = (400 - buttsizex / 2, 10)
            coords = [first_coords[0], first_coords[1]]
            for i in win_text:
                if i == 'Главное меню' or i == 'Выйти':
                    Buttons.append(Button(screen, coords[0], coords[1], buttsizex, buttsizey,
                                          func=funcs[-(len(win_text) - win_text.index(i))]))
                string_rendered = font.render(i, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = coords[1] + buttsizey / 2 - font.size(i)[1] / 2
                intro_rect.x = coords[0] + buttsizex / 2 - font.size(i)[0] / 2
                Text.append([string_rendered, intro_rect])
                coords[1] += 80
            for bn in Buttons:
                bn.draw()
            for tt in Text:
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


def start(level):
    first_player, second_player, level_x, level_y = generate_level(level)
    size = WIDTH, HEIGHT = (800, 450)
    screen = pygame.display.set_mode(size)

    running = True
    clock = pygame.time.Clock()
    FPS = 300
    coordbutt = [50, 50]
    pause_button = Button(screen, 0, 0, 50, 50, func=pause_window)

    while running:
        for shell in shells_group:
            if shell.rect.right < 0 or shell.rect.left > WIDTH or shell.rect.top > HEIGHT or shell.rect.bottom < 0:
                shell.kill()
        if first_player.health <= 0 or second_player.health <= 0:
            if first_player.health > 0:
                running = False
                for i in range(1, 26):
                    image = pygame.image.load(rf'.\data\boom{i}.png')
                    time.sleep(0.05)
                    screen.blit(image, (second_player.rect.x, second_player.rect.y))
                    pygame.display.flip()
                win_screen('Первый игрок')
                return
            elif second_player.health > 0:
                running = False
                for i in range(1, 26):
                    image = pygame.image.load(rf'.\data\boom{i}.png')
                    time.sleep(0.05)
                    screen.blit(image, (first_player.rect.x, first_player.rect.y))
                    pygame.display.flip()
                win_screen('Второй игрок')
                return
            else:
                win_screen('Ничья')
                return

        # delta_time = clock.tick(FPS) / 1000
        pause_button.draw()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                answ = pause_button.act()
                if answ != None:
                    answ()
                break
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == pygame.KEYDOWN:

                # Движение и стрельба первого танка
                if first_player.health > 0 and second_player.health > 0:
                    if event.key == getattr(pygame, 'K_' + bind_dict[first_up_down_left_right_fire_key[0]]):
                        if first_player.speed < 0:
                            first_player.speed *= -1
                        first_player.moving = True
                    if event.key == getattr(pygame, 'K_' + bind_dict[first_up_down_left_right_fire_key[1]]):
                        first_player.moving = True
                        if first_player.speed > 0:
                            first_player.speed *= -1
                    if event.key == getattr(pygame, 'K_' + bind_dict[first_up_down_left_right_fire_key[2]]):
                        if first_player.rotating_angle < 0:
                            first_player.rotating_angle *= -1
                        first_player.rotating = True
                    if event.key == getattr(pygame, 'K_' + bind_dict[first_up_down_left_right_fire_key[3]]):
                        if first_player.rotating_angle > 0:
                            first_player.rotating_angle *= -1
                        first_player.rotating = True
                    if (event.key == getattr(pygame, 'K_' + bind_dict[first_up_down_left_right_fire_key[4]]) and
                            first_player.health > 0):
                        first_player.shoot()
                        # shell_flying = True

                    # Движение и стрельба второго танка

                    if event.type == pygame.KEYDOWN:
                        if event.key == getattr(pygame, 'K_' + bind_dict[second_up_down_left_right_fire_key[0]]):
                            if second_player.speed < 0:
                                second_player.speed *= -1
                            second_player.moving = True
                        if event.key == getattr(pygame, 'K_' + bind_dict[second_up_down_left_right_fire_key[1]]):
                            second_player.moving = True
                            if second_player.speed > 0:
                                second_player.speed *= -1
                        if event.key == getattr(pygame, 'K_' + bind_dict[second_up_down_left_right_fire_key[2]]):
                            if second_player.rotating_angle < 0:
                                second_player.rotating_angle *= -1
                            second_player.rotating = True
                        if event.key == getattr(pygame, 'K_' + bind_dict[second_up_down_left_right_fire_key[3]]):
                            if second_player.rotating_angle > 0:
                                second_player.rotating_angle *= -1
                            second_player.rotating = True

                        if event.key == getattr(pygame, 'K_' + bind_dict[
                            second_up_down_left_right_fire_key[4]]) and second_player.health > 0:
                            second_player.shoot()

                            # shell_flying = True

            if event.type == pygame.KEYUP:

#             # Остановка первого танка

                keys = pygame.key.get_pressed()
                if event.key == getattr(pygame, 'K_' + bind_dict[first_up_down_left_right_fire_key[2]]):
                    if not keys[getattr(pygame, 'K_' + bind_dict[first_up_down_left_right_fire_key[3]])]:
                        first_player.rotating = False
                    elif first_player.rotating_angle > 0:
                        first_player.rotating_angle *= -1
                if event.key == getattr(pygame, 'K_' + bind_dict[first_up_down_left_right_fire_key[3]]):
                    if not keys[getattr(pygame, 'K_' + bind_dict[first_up_down_left_right_fire_key[2]])]:
                        first_player.rotating = False
                    elif first_player.rotating_angle < 0:
                        first_player.rotating_angle *= -1
                if event.key == getattr(pygame, 'K_' + bind_dict[first_up_down_left_right_fire_key[0]]):
                    first_player.moving = False
                if event.key == getattr(pygame, 'K_' + bind_dict[first_up_down_left_right_fire_key[1]]):
                    first_player.moving = False

                # Остановка второго танка

                if event.type == pygame.KEYUP:
                    keys = pygame.key.get_pressed()
                    if event.key == getattr(pygame, 'K_' + bind_dict[second_up_down_left_right_fire_key[2]]):
                        if not keys[getattr(pygame, 'K_' + bind_dict[second_up_down_left_right_fire_key[3]])]:
                            second_player.rotating = False
                        elif second_player.rotating_angle > 0:
                            second_player.rotating_angle *= -1
                    if event.key == getattr(pygame, 'K_' + bind_dict[second_up_down_left_right_fire_key[3]]):
                        if not keys[getattr(pygame, 'K_' + bind_dict[second_up_down_left_right_fire_key[2]])]:
                            second_player.rotating = False
                        elif second_player.rotating_angle < 0:
                            second_player.rotating_angle *= -1
                    if event.key == getattr(pygame, 'K_' + bind_dict[second_up_down_left_right_fire_key[0]]):
                        second_player.moving = False
                    if event.key == getattr(pygame, 'K_' + bind_dict[second_up_down_left_right_fire_key[1]]):
                        second_player.moving = False

        all_sprites.update()

        screen.fill(pygame.Color('black'))
        tiles_group.draw(screen)
        shells_group.draw(screen)
        player_group.draw(screen)

        pygame.draw.rect(screen, (80, 80, 80), (0, 0, 50, 50))
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, 50, 50), 3)
        string_rendered = font.render('||', 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 25 - font.size('||')[1] / 2
        intro_rect.x = 25 - font.size('||')[0] / 2
        if 0 <= pygame.mouse.get_pos()[0] <= 50 and 0 <= pygame.mouse.get_pos()[1] <= 50:
            pygame.draw.rect(screen, (120, 120, 120), (0, 0, 50, 50), 3)
        screen.blit(string_rendered, intro_rect)

        pygame.display.flip()

        clock.tick(FPS)

    return


class Timer:
    import time
    def __init__(self):
        self.start()

    def start(self):
        self.t = Timer.time.time()

    def __call__(self):
        return Timer.time.time() - self.t


class Button:
    def __init__(self, space, x, y, sizex, sizey, func=None, firstkey=None):
        self.sizex = sizex
        self.sizey = sizey
        self.coords = (x, y)
        self.func = func
        self.space = space
        self.key = firstkey

    def act(self):
        if self.coords[0] <= pygame.mouse.get_pos()[0] <= self.coords[0] + self.sizex and \
                self.coords[1] <= \
                pygame.mouse.get_pos()[1] <= self.coords[1] + self.sizey:
            if self.func != 'changeloud+' and self.func != 'changeloud-':
                pygame.draw.rect(screen, (20, 20, 20),
                                 (self.coords[0] + 3, self.coords[1] + 3, self.sizex - 6, self.sizey - 6), 5)
                pygame.display.flip()

                time.sleep(0.15)
            if self.func != None and type(self.func) != str:
                return self.func
            elif type(self.func) == str:
                if self.func in 'changebutt1' + 'changebutt2':

                    clicked = False
                    t = Timer()
                    t.start()
                    while not clicked or int(t.__call__()) < 5:

                        if int(t.__call__()) == 3 or clicked:
                            break
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                key = pygame.key.name(event.key).capitalize()
                                if '[' in key:
                                    key = key[1] + '^'
                                if key not in second_up_down_left_right_fire_key + first_up_down_left_right_fire_key:
                                    clicked = True

                    if clicked:
                        if self.func == 'changebutt1':
                            first_up_down_left_right_fire_key[
                                first_up_down_left_right_fire_key.index(self.key)] = key.capitalize()
                        if self.func == 'changebutt2':
                            second_up_down_left_right_fire_key[
                                second_up_down_left_right_fire_key.index(self.key)] = key.capitalize()
                        self.key = key
                        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                        pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
                if self.func in 'changeloud+' + 'changeloud-':
                    settings.change_loud(self.func)
                if self.func == 'quit':
                    return self.func
                if self.func == 'start':
                    return 'start'
        else:
            return None

    def retfunc(self):
        return self.func

    def draw(self):
        pygame.draw.rect(self.space, (80, 80, 80), (self.coords[0], self.coords[1], self.sizex, self.sizey))
        pygame.draw.rect(self.space, (50, 50, 50), (self.coords[0], self.coords[1], self.sizex, self.sizey), 3)
        if self.coords[0] <= pygame.mouse.get_pos()[0] <= self.coords[0] + self.sizex and self.coords[1] <= \
                pygame.mouse.get_pos()[1] <= self.coords[1] + self.sizey:
            pygame.draw.rect(screen, (120, 120, 120), (self.coords[0], self.coords[1], self.sizex, self.sizey), 3)


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
    global countmap, wins, running, start_time
    wins['first'] = 0
    wins['second'] = 0
    countmap = 0
    intro_text = ["Начать игру",
                  "Правила игры",
                  "Настройки",
                  "Информация",
                  "Выйти"]
    funcs = ['start', rule_screen, set_screen, info_screen, 'quit']
    Buttons = []
    text = []
    x = (WIDTH // 2) - 150
    y = 50
    buttwidth, buttheight = [270, 50]
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
                            running = True
                            start_time = time.gmtime()
                            start(load_level(maps[countmap]))
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
    global sound_level, pause
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
                            if 'changebutt' in bt.retfunc():
                                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                                pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
                            bt.act()
                            b = bt.retfunc()

        string_rendered = font.render(str(settings.sound_level), 1, pygame.Color('white'))
        butt_rect = string_rendered.get_rect()
        butt_rect.x = 400 - font.size(str(settings.sound_level))[0] / 2
        butt_rect.top = butty2
        screen.blit(string_rendered, butt_rect)
        pygame.display.flip()

        clock.tick(FPS)


def rule_screen():
    rule_text = ["Правила игры",
                 "Первый танк",
                 f"Перемещается при зажатии клавиш {', '.join(first_up_down_left_right_fire_key[:-1])}.",
                 f"Стрельба производится по нажатии кнопки {first_up_down_left_right_fire_key[-1]}, после",
                 "чего происходит перезарядка длительностью в 4 секунды",
                 "Второй танк",
                 f"Перемещается при зажатии клавиш {', '.join(second_up_down_left_right_fire_key[:-1])}.",
                 f"Стрельба производится по нажатии кнопки {second_up_down_left_right_fire_key[-1]}, после",
                 "чего происходит перезарядка длительностью в 4 секунды"]
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


def generate_level(level):
    global all_sprites, box_group, wall_group, tiles_group, player_group, shells_group, first_player, second_player
    all_sprites = pygame.sprite.Group()
    box_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    shells_group = pygame.sprite.Group()
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
    def __init__(self, pos_x, pos_y, angle, tank):
        super().__init__(shells_group, all_sprites)
        self.original_image = shell_image
        self.image = shell_image.copy()
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.angle = angle
        self.speed = 4.6
        self.tank = tank  # сохраняем ссылку на танк, который выпустил снаряд
        self.image = pygame.transform.rotate(self.original_image, degrees(self.angle - pi / 2))
        self.rect = self.image.get_rect(center=self.rect.center)  # устанавливаем центр изображения как точку поворота
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        for tile in pygame.sprite.spritecollide(self, box_group, False, pygame.sprite.collide_mask):
            tile.destroy()
            self.kill()
        for tile in pygame.sprite.spritecollide(self, wall_group, False, pygame.sprite.collide_mask):
            self.kill()
        for player in pygame.sprite.spritecollide(self, player_group, False):
            if player != self.tank:  # проверяем, что снаряд не столкнулся с танком, который его выпустил
                # наносим урон танку
                player.health -= 40
                if player.health <= 0:
                    # если здоровье танка стало меньше или равно 0, то танк уничтожается
                    player.kill()

                self.kill()  # убиваем снаряд
        self.rect.centerx += round(self.speed * cos(self.angle))
        self.rect.centery -= round(self.speed * sin(self.angle))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player, health=100):
        super().__init__(player_group, all_sprites)

        self.player = player
        self.health = health

        self.reload_time = 500
        self.last_shot_time = pygame.time.get_ticks() - self.reload_time

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

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.reload_time:
            # создание и запуск пули
            shell = TankShell(self.rect.centerx, self.rect.centery, self.angle, self)
            self.last_shot_time = current_time


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
                            if funcs.index(bn.retfunc()) == 2:
                                first_player.kill()
                                second_player.kill()
                                running = False
                            pause = True
                            answ()
                            return

        pygame.display.flip()
        clock.tick(FPS)


start_screen()
