#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
p = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
print("inserting to sys.path: ", p)
sys.path.insert(0, p)
# print sys.path

import os
import unittest

import tiledtmxloader


_has_pygame = False
try:
    import pygame
    _has_pygame = True
    import tiledtmxloader.helperspygame
except:
    pass

    
class MapLoadTestsPygame(unittest.TestCase):

    def setUp(self):
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        if not _has_pygame:
            self.fail("needs either module 'pygame' installed for testing")
        self.resourceloader = tiledtmxloader.helperspygame.ResourceLoaderPygame()
        
        
    def test_tile_properties(self):
        self.fail("implement test!! (load map with tile properties and read a tile proerty from test")
        
    def test_wrong_sized_tileset(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("map.tmx")
            self.resourceloader.load(world_map)
            num_images = len(self.resourceloader.indexed_tiles)
            self.assertTrue(num_images == 120, "should be 120 tiles, wrong number of tile images loaded: " + str(num_images))
            
    def test_load_unkown_version_should_raise_exception(self):
        try:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("invalid_version.tmx")
            self.fail("should have raised an exception because of wrong version")
        except tiledtmxloader.tmxreader.VersionError as e:
            pass
        except Exception as ex:
            self.fail("should be a VersionError exception, not: " + str(ex))

    
        
    #--- pygame tests ---#
    def test_load_map_from_cur_dir(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("minix.tmx")
            self.resourceloader.load(world_map)

    def test_load_map_from_cur_dir_using_tsx(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("minix_using_tsx.tmx")
            self.resourceloader.load(world_map)

    def test_load_map_from_sub_dir_using_tsx(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("mini2/mini2.tmx")
            self.resourceloader.load(world_map)

    def test_load_map_from_sub_dir(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("mini2/mini2_alt.tmx")
            self.resourceloader.load(world_map)

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("mini3/mini3.tmx")
            self.resourceloader.load(world_map)

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_and_img_from_sub_dir(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("mini4/mini4.tmx")
            self.resourceloader.load(world_map)

    def test_can_load_compression_xml(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("minix_xml.tmx")
            self.resourceloader.load(world_map)

    def test_can_load_compression_cvs(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("minix_cvs.tmx")
            self.resourceloader.load(world_map)

    def test_can_load_compression_base64_zlib(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("minix_base64_zlib.tmx")
            self.resourceloader.load(world_map)

    def test_can_load_compression_base64_uncompressed(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("minix_base64_uncompressed.tmx")
            self.resourceloader.load(world_map)

    def test_can_load_compression_base64_gzip(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("minix_base64_gzip.tmx")
            self.resourceloader.load(world_map)

    def test_can_load_compression_base64_gzip_dtd(self):
        if _has_pygame:
            world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("minix_base64_gzip_dtd.tmx")
            self.resourceloader.load(world_map)
            
    def test_get_list_of_quad_coords(self):
        if _has_pygame:
            layer = tiledtmxloader.helperspygame.SpriteLayer
            coords = layer._get_list_of_neighbour_coord(0, 0, 1, 10, 10)
            expected = ((0, 0), )
            self.compare(expected, coords)
            
            coords = layer._get_list_of_neighbour_coord(0, 0, 2, 10, 10)
            expected = ((0, 0), (1, 0), (0, 1), (1, 1))
            self.compare(expected, coords)
            
            coords = layer._get_list_of_neighbour_coord(1, 1, 3, 10, 10)
            expected = ((3, 3), (4, 3), (5, 3), (3, 4), (4, 4), (5, 4), (3, 5), (4, 5), (5, 5))
            self.compare(expected, coords)
            
    def compare(self, expected, captured):
        """
        Helper method to compare to lists.
        """
        if len(expected) != len(captured):
            self.fail(str.format("Not same number of expected and captured actions! \n expected: {0} \n captured: {1}", \
                                    ", ".join(map(str, expected)), \
                                    ", ".join(map(str, captured))))
        for idx, expected_action in enumerate(expected):
            action = captured[idx]
            if action != expected_action:
                self.fail(str.format("captured action does not match with expected action! \n expected: {0} \n captured: {1}", \
                                    ", ".join(map(str, expected)), \
                                    ", ".join(map(str, captured))))

    
#  -----------------------------------------------------------------------------

_has_pyglet = False
try:
    import pyglet
    _has_pyglet = True
    import tiledtmxloader.helperspyglet
except:
    pass


class MapLoadTestsPyglet(MapLoadTestsPygame):

    def setUp(self):
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        if not _has_pyglet:
            self.fail("needs either module 'pyglet' installed for testing")
        self.resourceloader = tiledtmxloader.helperspyglet.ResourceLoaderPyglet()
            


if __name__ == '__main__':
    unittest.main()
            