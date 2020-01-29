import tiledtmxloader
from . import  sprites
import pygame
import os


class TMX:

    def __init__(self, file='map.tmx'):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        #file = os.path.join(), file)
        world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file)
        self.resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
        self.resources.load(world_map)
        self.sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(self.resources)
        self.W = self.sprite_layers[0].num_tiles_x
        self.H = self.sprite_layers[1].num_tiles_y
        self.parse()

    def parse(self):
        tmx = [sprites.background, sprites.walls]
        W = self.W
        H = self.H
        self.lvl = [[' ' for i in range(4 * W)] for _ in range(4 * H)]
        for i in range(len(tmx)):
            layer = self.sprite_layers[i]
            for row in range(0, layer.num_tiles_x):
                for col in range(0, layer.num_tiles_y):
                    if layer.content2D[col][row] is not None:
                        if tmx[i] == sprites.walls:
                            for x in range(2):
                                if 2 * row - 1 >= 0:
                                    self.lvl[2 * col + x][2 * row - 1] = '-'
                                self.lvl[2 * col + x][2 * row] = '-'
                                self.lvl[2 * col + x][2 * row + 1] = '-'
                        tmp = sprites.Sprite(layer.content2D[col][row].image, tmx[i])
                        tmp.move(row * 32, col * 32)

        layer = self.sprite_layers[2]
        for door in layer.objects:
            d = sprites.Door(['tmp/4.png', 'tmp/5.png', 'tmp/6.png', 'tmp/7.png'])
            d.move(door.x // 32 * 32, door.y // 32 * 32)
            d.open = int(door.properties["open"])
            row = door.x // 32
            col = door.y // 32
            for x in range(2):
                if 2 * row - 1 >= 0:
                    self.lvl[2 * col + x][2 * row - 1] = '-'
                    self.lvl[2 * col + x][2 * row] = '-'
                    self.lvl[2 * col + x][2 * row + 1] = '-'
        layer = self.sprite_layers[3]
        for person_ in layer.objects:
            if person_.properties["img"] == "person.png":
                self.person = sprites.CharacterSprite(pygame.image.load(
                    "person.png"), person_.x, person_.y, True, sprites.character)
            else:
                sprites.CharacterSprite(
                    pygame.image.load(
                        person_.properties["img"]
                    ),
                    person_.x,
                    person_.y,
                    False,
                    sprites.character
                )