import pygameMenu
import copy

import tiledtmxloader
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
import math

world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode('map.tmx') 
resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
resources.load(world_map)
sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)


tmx = [sprites.background, sprites.walls, sprites.doors]

W = sprite_layers[0].num_tiles_x
H = sprite_layers[1].num_tiles_y
lvl = [[' ' for i in range(4 * W)] for _ in range(4 * H)]

for i in range(len(tmx)):
    layer = sprite_layers[i] 
    for row in range(0, layer.num_tiles_x): # перебираем все координаты тайлов
        for col in range(0, layer.num_tiles_y): # перебираем все координаты тайлов
            if layer.content2D[col][row] is not None:
                if tmx[i] == sprites.walls or tmx[i] == sprites.doors: 
                    for x in range(2):
                        if 2 * row - 1 >= 0:
                            lvl[2 * col + x][2 * row - 1] = '-'
                        lvl[2 * col + x][2 * row] = '-'
                        lvl[2 * col + x][2 * row + 1] = '-'
                           
                tmp = sprites.Sprite(layer.content2D[col][row].image, tmx[i])
                tmp.move(row * 32, col * 32)

layer = sprite_layers[3] 
for person in layer.objects:
    if person.properties["img"] == "person.png":
        person = sprites.CharacterSprite(pygame.image.load("person.png"), person.x, person.y, True, sprites.character)
    else:
        person = sprites.CharacterSprite(pygame.image.load(person.properties["img"]), person.x, person.y, False, sprites.character)


a = 135

size = ((W + 1) * 32, (H + 1) * 32)

pygame.init()
screen = pygame.display.set_mode(size)#, pygame.FULLSCREEN)


clock = pygame.time.Clock()


# https://github.com/TheAlgorithms/Python/blob/master/graphs/bfs_shortest_path.py

def bfs_shortest_path(graph: dict, start, goal) -> str:
    explored = []
    queue = [[start]]
    if start == goal:
        return -1
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                if neighbour == goal:
                    return new_path
            explored.append(node)
    return -1


class Engine():

    def __init__(self):
        self.obj = []

    def check(self, x, y):
        # https://mrtsepa.gitbooks.io/pygame-tutorial/content/reference/pygame/masks.html
        for wall in sprites.walls:
            offset = (wall.rect.x - person.rect.x - x, wall.rect.y - person.rect.y - y)
            if person.mask.overlap_area(wall.mask, offset) > 0:
                return False
        return True

    def move(self, i):
        if i == 0 and self.check(0, -1):
            person.rect = person.rect.move(0, -1) 
            person.w()
        elif i == 1 and self.check(1, -1):
            person.rect = person.rect.move(1, -1)
            person.w()
        elif i == 2 and self.check(1, 0): 
            person.rect = person.rect.move(1, 0)
            person.d()
        elif i == 3 and self.check(1, 1): 
            person.rect = person.rect.move(1, 1)
            person.d()
        elif i == 4 and self.check(0, 1): 
            person.rect = person.rect.move(0, 1)
            person.s()
        elif i == 5 and self.check(-1, 1): 
            person.rect = person.rect.move(-1, 1)
            person.s()
        elif i == 6 and self.check(-1, 0): 
            person.rect = person.rect.move(-1, 0)
            person.a()
        elif i == 7 and self.check(-1, -1): 
            person.rect = person.rect.move(-1, -1)
            person.a()
        else:
            return False
        return True

    def key(self, w, a, s, d):  
        if w and a:
            res = self.move(7)
            if not res:
                res = self.move(0)
                if not res:
                    self.move(6)
        elif s and a:
            res = self.move(5)
            if not res:
                res = self.move(4)
                if not res:
                    self.move(6)
        elif d and s:
            res = self.move(3)
            if not res:
                res = self.move(4)
                if not res:
                    self.move(2)
        elif w and d:
            res = self.move(1)
            if not res:
                res = self.move(0)
                if not res:
                    self.move(2)
        elif w:
            self.move(0)
        elif a:
            self.move(6)
        elif s:
            self.move(4)
        elif d:
            self.move(2)
    
    def attack(self, angle):
        angle = angle % 360
        if 315 <= angle <= 360 or  0 <= angle<= 45:
            person.d_attack()
        elif 45 < angle <= 135:
            person.w_attack()
        elif 135 < angle <= 225:
            person.a_attack()
        else:
            person.s_attack()


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

engine = Engine()

thread = KeyBoard(engine)
thread.start()


pygame.mouse.set_cursor((24, 24), (7, 0), cursor.curs, cursor.mask)

def scalar(x1, y1, x2, y2):
    return x1 *  x2 + y1 * y2
 
def module(x, y):
    return math.sqrt(x ** 2 + y ** 2)


  
graph = {}
for i in range(len(lvl)):
    for j in range(len(lvl[i])):    
        if lvl[i][j] != '-':
            graph[i * len(lvl[0]) + j] = []
            if 0 <= i - 1 and lvl[i - 1][j] != '-':
                graph[i * len(lvl[0]) + j].append((i - 1) * len(lvl[0]) + j)
            if  0 <= j - 1  and lvl[i][j - 1] != '-':
                graph[i * len(lvl[0]) + j].append(i * len(lvl[0]) + j - 1)
            if  j + 1 < len(lvl[i]) and lvl[i][j + 1] != '-':
                graph[i * len(lvl[0]) + j].append(i * len(lvl[0]) + j + 1)
            if i + 1 < len(lvl) and lvl[i + 1][j] != '-':
                graph[i * len(lvl[0]) + j].append((i + 1) * len(lvl[0]) + j)


fps_block = -1
angle_attack = 0

def atack(x, y):
    x2 = x - person.rect.x - 32
    y2 = - y + person.rect.y + 32
    cos1 = scalar(100, 0, x2, y2)  /  (module(100, 0) * module(x2,y2))
    cos2 = scalar(0, 100, x2, y2) / (module(0, 100) *  module(x2,y2))
    ang1 = math.degrees(math.acos(cos1))
    ang2 = math.degrees(math.acos(cos2))
    if ang2 < 90:
        angle = math.degrees(math.acos(cos1))
    else:
        angle = 360 - math.degrees(math.acos(cos1))
    arrow = sprites.AroowSprite(pygame.image.load("tmp/270.png"))
    arrow.rotate_c((angle + a) % 360)
    arrow.rect.center = person.rect.center
    lenght = math.sqrt(x2** 2 + y2 ** 2)
    k = lenght / 15
    l = 1 / (k - 1)
    arrow.dx = (l * x2) / (1 + l)
    arrow.dy = -(l * y2) / (1 + l)
    person.cur_frame = 0
    return angle

old_graph = copy.deepcopy(graph)

while True:
    graph = copy.deepcopy(old_graph)

    screen.unlock()
    clock.tick(60)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
    screen.fill(pygame.Color(109, 170, 44))
    # draw sprites
    sprites.background.draw(screen)
    sprites.character_death.draw(screen)
    sprites.aroows.draw(screen)
    sprites.walls.draw(screen)
    sprites.character.draw(screen)
    sprites.doors.draw(screen)

    if fps_block == 12 * 3:
        fps_block = -1
    if fps_block != -1:
        fps_block += 1
        if fps_block % 3 == 0:
            thread.engine.attack(angle_attack)

    keys = thread.keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os._exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and fps_block == -1:
                angle_attack = atack(x, y)
                fps_block = 0
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            
    if keys[K_ESCAPE]:
        os._exit(0)
    if  fps_block == -1 and sum([keys[K_w], keys[K_a], keys[K_s], keys[K_d]]):
        for i in range(5):
            thread.engine.key(keys[K_w], keys[K_a], keys[K_s], keys[K_d])

    for aroow in sprites.aroows:
        for obj in sprites.doors:
            offset = (aroow.rect.x - obj.rect.x + int(aroow.dx), aroow.rect.y - obj.rect.y + int(aroow.dy))
            if obj.mask.overlap_area(aroow.mask, offset) > 0:
                aroow.kill()
                break

    for aroow in sprites.aroows:
        for obj in sprites.character:
            offset = (aroow.rect.x - obj.rect.x + int(aroow.dx), aroow.rect.y - obj.rect.y + int(aroow.dy))
            if not obj.main_person and obj.mask.overlap_area(aroow.mask, offset) > 0:
                aroow.kill()
                obj.xp -= 100
                break

    for aroow in sprites.aroows:
        for obj in sprites.walls:
            offset = (aroow.rect.x - obj.rect.x + int(aroow.dx), aroow.rect.y - obj.rect.y + int(aroow.dy))
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

    start = ((person.rect.y) // 16 + 1) * len(lvl[0]) + (person.rect.x + 1) // 16 + 1

    lvl[start // len(lvl[0])][start % len(lvl[0])] = 'k'


    for cur in sprites.character:
        if not cur.main_person:
            if cur.fps_draw % 5 == 0:
                to = ((cur.rect.y) // 16 + 1) * len(lvl[0]) + (cur.rect.x + 1) // 16 + 1           
                #for i in range(5):
                #    for j in range(3):
                #        vertex = to + (i - 1) * len(lvl[0]) + j
                #        lvl[vertex // len(lvl[0])][vertex % len(lvl[0])] = 'k'          
                
                cur = to
                for i in range(3):
                    for j in range(3):
                        vertex = to + i * len(lvl[0]) + j
                        lvl[vertex // len(lvl[0])][vertex % len(lvl[0])] = 'k' 
                        if vertex in graph and cur in graph[vertex]:
                            graph[vertex].remove(cur)

                

    for cur in sprites.character:
        if not cur.main_person:
            if cur.fps_draw % 5 == 0:
                to = ((cur.rect.y) // 16 + 1) * len(lvl[0]) + (cur.rect.x + 1) // 16 + 1                
                res = bfs_shortest_path(graph, to, start)
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
            character_death = sprites.CharacterSprite(cur.main_sheet, 0, 0, False, sprites.character_death)
            character_death.move(cur.rect.x, cur.rect.y)
            cur.kill()
        else:
            pygame.draw.rect(screen, pygame.Color('red'), (cur.rect.x + 3, cur.rect.y, 58, 10), 1)
            pygame.draw.rect(screen, pygame.Color('red'), (cur.rect.x + 3 , cur.rect.y, 58 * (cur.xp / 100), 10))

    for cur in sprites.character:
        if not cur.main_person:
            offset = (cur.rect.x - person.rect.x, cur.rect.y - person.rect.y)
            if cur.mask.overlap_area(person.mask, offset) > 0:
                cur.kill()
                person.xp -= 30
    
    for i in range(len(lvl)):
        for j in range(len(lvl[0])):
            if lvl[i][j] == '-':
                pygame.draw.rect(screen, pygame.Color('red'), (j * 16, i * 16, 16, 16), 1)
            elif lvl[i][j] == ' ':
                pygame.draw.rect(screen, pygame.Color('green'), (j * 16, i * 16, 16, 16), 1)
            else:
                pygame.draw.rect(screen, pygame.Color('blue'), (j * 16, i * 16, 16, 16), 1)
    pygame.display.flip()

