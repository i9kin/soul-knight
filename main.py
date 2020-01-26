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


from tmx import TMX
from engine import Engine, Camera
import graph

sys.setrecursionlimit(100000000)

t = TMX()
lvl = t.lvl
person = t.person

size = ((t.W + 1) * 32, (t.H + 1) * 32)
pygame.init()
screen = pygame.display.set_mode(size)  # , pygame.FULLSCREEN)
clock = pygame.time.Clock()


class KeyBoard(threading.Thread):

    def __init__(self, engine):
        super().__init__()
        self.engine = engine

    def run(self):
        self.alive = True
        while self.alive:
            self.keys = pygame.key.get_pressed()
            time.sleep(0.01)
            pygame.event.pump()

    def stop(self):
        self.alive = False
        self.join()


engine = Engine(person)

thread = KeyBoard(engine)
thread.start()

pygame.mouse.set_cursor((24, 24), (7, 0), cursor.curs, cursor.mask)

q = graph.G(lvl)
game_graph = q.graph
colors = q.colors


fps_block = -1
angle_attack = 0
play_game = True


camera = Camera([sprites.background, sprites.character_death,
                 sprites.aroows, sprites.walls, sprites.doors], 200, 200)



while True:
    screen.unlock()
    clock.tick(60)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
    screen.fill(pygame.Color(109, 170, 44))
    if not play_game:
        pygame.display.flip()
        continue

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
            thread.engine.attack_anim(angle_attack)

    keys = thread.keys
    for event in pygame.event.get():
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
            thread.engine.key(keys[K_w], keys[K_a], keys[K_s], keys[K_d])
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
