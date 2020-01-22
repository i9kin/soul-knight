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
    Example showing basic loading and rendering of a tmx map.
    """

    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)

    # init pygame and set up a screen
    pygame.init()
    pygame.display.set_caption("tiledtmxloader - " + file_name + " - keys: arrows" )
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

    # variables for the main loop
    frames_per_sec = 60.0
    clock = pygame.time.Clock()
    running = True

    # mainloop
    while running:
        clock.tick(frames_per_sec)

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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


        # adjust camera to position according to the keypresses
        renderer.set_camera_position(cam_world_pos_x, \
                                     cam_world_pos_y, "topleft")

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


