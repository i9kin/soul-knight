
LICENSES

    - The map "001-1.tmx" and its tilesets are under the GPL2+ license!
    - The examples itself are undder the "New BSD license"



Welcome the the examples for the tiledtmxloader version 3.X

Unfortunately I had not time to implement the pyglet parts, so
this examples are all pygame only.

There is a map included from the game "The mana world" [http://themanaworld.org/].
It is called "001-1.tmx" and is placed next to this README file.


This map allows to show most of the features of this release. It is
automatically used if you start the examples without argument. If you wish
to start any example with another map, you can provide it as first argument:

    >python 00_load_map.py ../mymap.tmx

To see how the provided map is structered, I recommend
to load it into "Tiled" and take a look at its layers.


The examples are divided into the following categories:

    00_load-a-map
        this examples show how to load a map and how to read certain
        properties out of the map
        
    01_resources_and_rendering
        this examples show how to load a map and then using a resoureloader
        and a renderer to actually bring the map on screen
        
    02_render_features
        this examples show what features the pygame renderer provides:
        enabling/disabling layers, scaling layers, parallax scrolling,
        collapsing layers and usage of dynamic sprites (sprites within a
        single layer that can move around)
        
    03_mini_game
        this examples show how to make the camera follow a dynamic
        sprite (I call it hero) and how you could use a collision
        layer for collision detection
        
If you have any question, suggestion, improvements or whatever feel
free to contact me through the project homepage or on IRC.
        
Enjoy!        

DR0ID @ 2009-2011

