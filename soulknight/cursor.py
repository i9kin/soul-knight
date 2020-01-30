import pygame
from pygame import *
from pygame.locals import *

clickhand = (  # 24x24
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "                        ",
    " XXXXXXXXX    XXXXXXXXX ",
    " XXXXXXXXX    XXXXXXXXX ",
    " XXXXXXXXX    XXXXXXXXX ",
    "                        ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "          XXXX          ",
    "                        ",
)

curs, mask = pygame.cursors.compile(clickhand, "X", ".")
