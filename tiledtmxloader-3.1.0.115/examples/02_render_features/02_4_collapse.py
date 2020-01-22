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
    This is the demo showing the usage of the collapse feature.
    """

    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)

    # init pygame and set up a screen
    pygame.init()
    pygame.display.set_caption("tiledtmxloader - " + file_name + \
                                                    " - keys: arrows, 0-9, r")
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

    # cam_offset is for scrolling
    cam_world_pos_x = 0
    cam_world_pos_y = 0

    # set initial cam position and size
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height, "topleft")

    # retrieve the layers
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

    # layer on/off keys
    num_keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, \
                    pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

    # variables for the main loop
    clock = pygame.time.Clock()
    running = True
    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # mainloop
    while running:
        clock.tick()

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                print("fps: ", clock.get_fps())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    cam_world_pos_y -= world_map.tileheight
                elif event.key == pygame.K_DOWN:
                    cam_world_pos_y += world_map.tileheight
                elif event.key == pygame.K_RIGHT:
                    cam_world_pos_x += world_map.tilewidth
                elif event.key == pygame.K_LEFT:
                    cam_world_pos_x -= world_map.tilewidth
                elif event.key == pygame.K_r:
                    print("resetting layers!")
                    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)
                elif event.key in num_keys:
                    # find out which layer to manipulate
                    idx = num_keys.index(event.key)
                    # make sure this layer exists
                    if idx < len(world_map.layers):
                        sprite_layers[idx] = tiledtmxloader.helperspygame.SpriteLayer.collapse(sprite_layers[idx])
                        print("layer %s has collapse level: %s" % \
                                 (idx, sprite_layers[idx].get_collapse_level()))
                    else:
                        print("no such layer or more than 10 layers: " + str(idx))

        # adjust camera to position according to the keypresses
        renderer.set_camera_position(cam_world_pos_x, cam_world_pos_y, "topleft")

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

if __name__ == '__main__':

    main()


