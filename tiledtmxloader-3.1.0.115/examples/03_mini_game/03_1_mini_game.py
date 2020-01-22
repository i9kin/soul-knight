#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

This is the pygame minimal example.

"""


__revision__ = "$Rev: 115 $"
__version__ = "3.0.0." + __revision__[6:-2]
__author__ = 'DR0ID @ 2009-2011'

import sys
import os
import math

import pygame

try:
    import _path
except:
    pass

import tiledtmxloader

#  -----------------------------------------------------------------------------

def main():
    """
    Main method.
    """
    args = sys.argv[1:]
    if len(args) < 1:
        path_to_map = os.path.join(os.pardir, "001-1.tmx")
        print(("usage: python %s your_map.tmx\n\nUsing default map '%s'\n" % \
            (os.path.basename(__file__), path_to_map)))
    else:
        path_to_map = args[0]

    demo_pygame(path_to_map)

#  -----------------------------------------------------------------------------

def demo_pygame(file_name):
    """
    Example showing how to use the paralax scrolling feature.
    """

    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)

    # init pygame and set up a screen
    pygame.init()
    pygame.display.set_caption("tiledtmxloader - " + file_name + \
                                                        " - keys: arrows, 0-9")
    screen_width = min(1024, world_map.pixel_width)
    screen_height = min(768, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))

    # load the images using pygame
    resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
    resources.load(world_map)

    # prepare map rendering
    assert world_map.orientation == "orthogonal"

    # renderer
    renderer = tiledtmxloader.helperspygame.RendererPygame()

    # create hero sprite
    # use floats for hero position
    hero_pos_x = screen_width
    hero_pos_y = screen_height
    hero = create_hero(hero_pos_x, hero_pos_y)

    # cam_offset is for scrolling
    cam_world_pos_x = hero.rect.centerx
    cam_world_pos_y = hero.rect.centery

    # set initial cam position and size
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height)

    # retrieve the layers
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

    # filter layers
    sprite_layers = [layer for layer in sprite_layers if not layer.is_object_group]

    # add the hero the the right layer, it can be changed using 0-9 keys
    sprite_layers[1].add_sprite(hero)

    # layer add/remove hero keys
    num_keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, \
                    pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

    # variables for the main loop
    clock = pygame.time.Clock()
    running = True
    speed = 0.075
    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # mainloop
    while running:
        dt = clock.tick()

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                print("fps: ", clock.get_fps())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in num_keys:
                    # find out which layer to manipulate
                    idx = num_keys.index(event.key)
                    # make sure this layer exists
                    if idx < len(world_map.layers):
                        if sprite_layers[idx].contains_sprite(hero):
                            sprite_layers[idx].remove_sprite(hero)
                            print("removed hero sprite from layer", idx)
                        else:
                            sprite_layers[idx].add_sprite(hero)
                            print("added hero sprite to layer", idx)
                    else:
                        print("no such layer or more than 10 layers: " + str(idx))

        # find directions
        direction_x = pygame.key.get_pressed()[pygame.K_RIGHT] - \
                                        pygame.key.get_pressed()[pygame.K_LEFT]
        direction_y = pygame.key.get_pressed()[pygame.K_DOWN] - \
                                        pygame.key.get_pressed()[pygame.K_UP]

        # make sure the hero moves with same speed in all directions (diagonal!)
        dir_len = math.hypot(direction_x, direction_y)
        dir_len = dir_len if dir_len else 1.0
        # update position
        hero_pos_x += speed * dt * direction_x / dir_len
        hero_pos_y += speed * dt * direction_y / dir_len
        hero.rect.midbottom = (hero_pos_x, hero_pos_y)

        # adjust camera according to the hero's position, follow him
        renderer.set_camera_position(hero.rect.centerx, hero.rect.centery)

        # clear screen, might be left out if every pixel is redrawn anyway
        screen.fill((0, 0, 0))

        # render the map
        for sprite_layer in sprite_layers:
            if sprite_layer.is_object_group:
                # we dont draw the object group layers
                # you should filter them out if not needed
                continue
            else:
                renderer.render_layer(screen, sprite_layer)

        pygame.display.flip()

#  -----------------------------------------------------------------------------

def create_hero(start_pos_x, start_pos_y):
    """
    Creates the hero sprite.
    """
    image = pygame.Surface((50, 70), pygame.SRCALPHA)
    image.fill((255, 0, 0, 200))
    rect = image.get_rect()
    rect.midbottom = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)

#  -----------------------------------------------------------------------------

if __name__ == '__main__':

    main()


