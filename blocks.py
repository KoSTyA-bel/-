#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)

class Platform(sprite.Sprite):
    def __init__(self, x, y, way = "%s/block/block.png" % ICON_DIR):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load(way).convert_alpha()
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/block/die.png" % ICON_DIR).convert_alpha()

class End(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/block/win.png" % ICON_DIR).convert_alpha()

class Half(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/block/H.png" % ICON_DIR).convert_alpha()
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT / 2)

class Magnit(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/block/magnit.png" % ICON_DIR).convert_alpha()

class Coin(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("block/coin.png")
        self.rect = Rect(x + 6, y + 6, PLATFORM_WIDTH-16, PLATFORM_HEIGHT)

# class Movable(Platform):
    # def __init__(self, x, y):
        # Platform.__init__(self, x, y)
        # self.image = image.load("block/move.png")
        # self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        # self.yvel = 0 # скорость вертикального перемещения
        # self.onGround = False # На земле ли я?

    # def move(self, xvel, platforms):
        # self.rect.x += xvel

    # def getY(self):
        # return(self.rect.y)
