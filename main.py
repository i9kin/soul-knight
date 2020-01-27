import pygameMenu
import pygame
from pygame import *
from pygame.locals import *
import random
import sprites
import threading
import sys
import time
import datetime
import cursor
import os
import time

from tmx import TMX
from engine import Engine, Camera
import graph


def quit():
    os._exit(0)


def main_background():
    pass


TIME = datetime.datetime.now() - datetime.datetime.now()
LAST_TIME = datetime.datetime.now()

cur_map = (1, 1)
size = (1000, 500)
pygame.init()
screen = pygame.display.set_mode(size)  # pygame.FULLSCREEN)
pygame.mouse.set_cursor((24, 24), (7, 0), cursor.curs, cursor.mask)
os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
sys.setrecursionlimit(100000000)

ABOUT = ['Author: 9kin']
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 100, 36)
test = False

MAIN_MENU = None


def update_level(value, enabled):
    global TIME, tmx, lvl, person, gr, game_graph, colors, fps_block, angle_attack, engine, cur_map, MAIN_MENU
    TIME = datetime.datetime.now() - datetime.datetime.now()
    cur_map = (value[0], 0)
    for sprite_group in camera.sprites:
        for sprite in sprite_group:
            sprite.kill()
    for sprite in sprites.character:
        sprite.kill()
    tmx = TMX(f'maps/map{value[0]}.tmx')
    lvl = tmx.lvl
    person = tmx.person
    engine = Engine(person)
    gr = graph.G(lvl)
    game_graph = gr.graph
    colors = gr.colors
    fps_block = -1
    angle_attack = 0
    update_time()
    MAIN_MENU.disable()
    MAIN_MENU = main_menu


def update_time():
    global LAST_TIME
    LAST_TIME = datetime.datetime.now()


def play_game():
    update_time()
    MAIN_MENU.disable()


def reset_game():
    update_time()
    update_level(cur_map, pygameMenu.events.CLOSE)


def back():
    update_time()
    MAIN_MENU.disable()


class KeyBoard(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        self.alive = True
        while self.alive:
            self.keys = pygame.key.get_pressed()
            time.sleep(0.01)
            pygame.event.pump()

    def stop(self):
        self.alive = False
        self.join()


thread = KeyBoard()
thread.start()
camera = Camera([sprites.background, sprites.character_death,
                 sprites.aroows, sprites.walls, sprites.doors], 200, 200)


def generate_menu(title, lines):
    about_menu = pygameMenu.TextMenu(screen,
                                     bgfun=main_background,
                                     color_selected=COLOR_WHITE,
                                     font=pygameMenu.font.FONT_BEBAS,
                                     font_color=COLOR_BLACK,
                                     font_size=30,
                                     font_size_title=40,
                                     menu_alpha=100,
                                     menu_color=MENU_BACKGROUND_COLOR,
                                     menu_height=int(size[1] * 0.7),
                                     menu_width=int(size[0] * 0.8),
                                     option_shadow=False,
                                     onclose=pygameMenu.events.CLOSE,
                                     title=title,
                                     window_height=size[1],
                                     window_width=size[0],
                                     enabled=False
                                     )
    for line in lines:
        if type(line) is str:
            about_menu.add_line(line)
        elif type(line) is list:
            about_menu.add_selector(line[0], line[1:-1], onchange=line[-1])
        else:
            about_menu.add_option(line[0], line[1])

    return about_menu


about_menu = generate_menu('about',
                           ['Author: 9kin',
                            ('Return to menu', pygameMenu.events.BACK)
                            ]
                           )

main_menu = generate_menu('main', [
    ('play', play_game),
    ('reset level', reset_game),
    ['level', ('1', 1), ('2', 2), update_level],
    ('about', about_menu),
    ('back', back),
    ('quit', quit)
]
)

win_menu = generate_menu('you win', [
    ('reset level', reset_game),
    ['level', ('1', 1), ('2', 2), update_level],
    ('quit', quit)
]
)

lose_menu = generate_menu('you lose', [
    ('reset level', reset_game),
    ['level', ('1', 1), ('2', 2), update_level],
    ('quit', quit)
]
)

MAIN_MENU = main_menu

reset_game()
first = 0

while True:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            os._exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                MAIN_MENU.enable()
    if first == 2:
        MAIN_MENU.enable()
        TIME = datetime.datetime.now() - datetime.datetime.now()
        LAST_TIME = datetime.datetime.now()
    first += 1

    MAIN_MENU.mainloop(events, disable_loop=test)
    if test:
        break
    TIME += datetime.datetime.now() - LAST_TIME
    LAST_TIME = datetime.datetime.now()
    pygame.display.set_caption(str(TIME))

    if len(sprites.character) == 1:
        MAIN_MENU = generate_menu('you win', [f'total time:{TIME}',
                                              ('reset level', reset_game),
                                              ['level', ('1', 1),
                                               ('2', 2), update_level],
                                              ('quit', quit)
                                              ])
        MAIN_MENU.enable()
    elif person.xp <= 0:
        MAIN_MENU = generate_menu('you lose', [f'total time:{TIME}',
                                               ('reset level', reset_game),
                                               ['level', ('1', 1),
                                                ('2', 2), update_level],
                                               ('quit', quit)
                                               ])

        MAIN_MENU.enable()

    screen.fill(pygame.Color(109, 170, 44))

    f = person.rect
    for door in sprites.doors:
        x1 = f.x + 16
        y1 = f.y + 16
        x2 = x1 + 32
        y2 = y1 + 48
        s = door.rect
        x3 = s.x
        y3 = s.y
        x4 = x3 + 32
        y4 = y3 + 32
        fr = pygame.Rect(x1 + camera.dx, y1 + camera.dy, 32, 48)
        sr = pygame.Rect(x3 + camera.dx, y3 + camera.dy, 32, 32)
        if fr.colliderect(sr):
            dy = 48 + (y1 - y3)
            dx = 32 + (x1 - x3)
            if (door.open == 0 or door.open == 2) and ((48 + (y3 - y1)) // 20 != 0):
                if door.open == 0:
                    door.image = door.frames[(48 + (y3 - y1)) // 20 - 1]
                elif door.open == 2:
                    door.image = door.frames[4 - ((48 + (y3 - y1)) // 20)]
            elif dx // 20 != 3:
                if door.open == 1:
                    door.image = door.frames[dx // 20 + 1]
                elif door.open == 3:
                    door.image = door.frames[3 - dx // 20]
        else:
            door.image = door.frames[0]

    camera.render(screen)

    start = ((person.rect.y) // 16 + 1) * \
        len(lvl[0]) + (person.rect.x + 15) // 16 + 1
    for ch in sprites.character:
        to = ((ch.rect.y) // 16 + 1) * len(lvl[0]) + (ch.rect.x + 15) // 16 + 1
        if colors[start] != colors[to]:
            ch.drawing = False
            continue
        ch.draw(screen, camera.dx, camera.dy)

    camera.dx = -person.rect.x + 500 - 32
    camera.dy = - person.rect.y + 250 - 32

    if fps_block == 12 * 3:
        person.s()
        fps_block = -1
    if fps_block != -1:
        fps_block += 1
        if fps_block % 3 == 0:
            engine.attack_anim(angle_attack)

    keys = thread.keys
    for event in events:
        if event.type == pygame.QUIT:
            os._exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and fps_block == -1:
                attack = True
                for obj in sprites.doors:
                    offset = (person.rect.x - obj.rect.x,
                              person.rect.y - obj.rect.y)
                    if obj.mask.overlap_area(person.mask, offset) > 0:
                        attack = False
                        break
                if attack:
                    angle_attack = engine.atack(x, y)
                    fps_block = 0
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            x -= camera.dx
            y -= camera.dy

    if fps_block == -1 and sum([keys[K_w], keys[K_a], keys[K_s], keys[K_d]]):
        for i in range(5):
            engine.key(keys[K_w], keys[K_a], keys[K_s], keys[K_d])
    elif fps_block == -1 and person.anim != 10:
        person.s()

    for aroow in sprites.aroows:
        for obj in sprites.doors:
            offset = (aroow.rect.x - obj.rect.x + int(aroow.dx),
                      aroow.rect.y - obj.rect.y + int(aroow.dy))
            if obj.mask.overlap_area(aroow.mask, offset) > 0:
                aroow.kill()
                break

    for aroow in sprites.aroows:
        for obj in sprites.character:
            offset = (aroow.rect.x - obj.rect.x + int(aroow.dx),
                      aroow.rect.y - obj.rect.y + int(aroow.dy))
            if not obj.main_person and obj.mask.overlap_area(aroow.mask, offset) > 0:
                aroow.kill()
                obj.xp -= 100
                break

    for aroow in sprites.aroows:
        for obj in sprites.walls:
            offset = (aroow.rect.x - obj.rect.x + int(aroow.dx),
                      aroow.rect.y - obj.rect.y + int(aroow.dy))
            if obj.mask.overlap_area(aroow.mask, offset) > 0:
                aroow.kill()
                break

    for aroow in sprites.aroows:
        aroow.rect = aroow.rect.move(aroow.dx, aroow.dy)

    for cur in sprites.character_death:
        cur.cnt_death += 1
        if cur.cnt_death == 6:
            cur.kill()
        else:
            cur.death()

    start = ((person.rect.y) // 16 + 1) * \
        len(lvl[0]) + (person.rect.x + 15) // 16 + 1
    lvl[start // len(lvl[0])][start % len(lvl[0])] = 'k'

    for cur in sprites.character:
        if not cur.main_person:
            if cur.fps_draw % 5 == 0:
                to = ((cur.rect.y) // 16 + 1) * \
                    len(lvl[0]) + (cur.rect.x + 15) // 16 + 1
                if colors[start] != colors[to]:
                    continue
                res = graph.bfs_shortest_path(game_graph, to, start)
                if res != -1:
                    x = res[1] % len(lvl[0]) * 16
                    y = res[1] // len(lvl[0]) * 16
                    delta_x = x - cur.rect.x - 16
                    delta_y = y - cur.rect.y - 16
                    if delta_y == -16:
                        cur.w()
                    elif delta_y == 16:
                        cur.s()
                    elif delta_x == 16:
                        cur.d()
                    else:
                        cur.a()
                    cur.rect = pygame.Rect(x - 16, y - 16, 16, 16)
            cur.fps_draw += 1

    for cur in sprites.character:
        if cur.xp <= 0:
            character_death = sprites.CharacterSprite(
                cur.main_sheet, 0, 0, False, sprites.character_death)
            character_death.move(cur.rect.x, cur.rect.y)
            cur.kill()
        elif cur.drawing:
            pygame.draw.rect(screen, pygame.Color(
                'red'), (cur.rect.x + 3 + camera.dx, cur.rect.y + camera.dy, 58, 10), 1)
            pygame.draw.rect(screen, pygame.Color(
                'red'), (cur.rect.x + 3 + camera.dx, cur.rect.y + camera.dy, 58 * (cur.xp / 100), 10))

    for cur in sprites.character:
        if not cur.main_person:
            offset = (cur.rect.x - person.rect.x, cur.rect.y - person.rect.y)
            if cur.mask.overlap_area(person.mask, offset) > 0:
                cur.kill()
                person.xp -= 30
    pygame.display.flip()
