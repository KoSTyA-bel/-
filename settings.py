import os
import pygame
from pygame import *

pygame.init()
font.init()

ICON_DIR = os.path.dirname(__file__)
#Window settings
WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

#Game name
GAME_NAME = "Alien adventure"

#Baclgound color
BACKGROUND_COLOR = "#000000"

#Sound in menu
SOUND_CHOISE = pygame.mixer.Sound("%s/levels/select.wav" % ICON_DIR)
SOUND_ACCEPT = pygame.mixer.Sound("%s/levels/accept.wav" % ICON_DIR)

#Player settings
MOVE_SPEED = 3.2
WIDTH = 22
HEIGHT = 32
COLOR =  "#888888"
JUMP_POWER = 8
GRAVITY = 0.35
ANIMATION_DELAY = 0.08

#Player animations
ANIMATION_RIGHT = [("%s/alien/0ralient.png" % ICON_DIR),
            ("%s/alien/1ralient.png" % ICON_DIR),
            ("%s/alien/2ralient.png" % ICON_DIR),
            ("%s/alien/1ralient.png" % ICON_DIR),
            ("%s/alien/0ralient.png" % ICON_DIR),
            ("%s/alien/3ralient.png" % ICON_DIR),
            ("%s/alien/4ralient.png" % ICON_DIR)]
ANIMATION_LEFT = [("%s/alien/0lalient.png" % ICON_DIR),
            ("%s/alien/1lalient.png" % ICON_DIR),
            ("%s/alien/2lalient.png" % ICON_DIR),
            ("%s/alien/1lalient.png" % ICON_DIR),
            ("%s/alien/0lalient.png" % ICON_DIR),
            ("%s/alien/3lalient.png" % ICON_DIR),
            ("%s/alien/4lalient.png" % ICON_DIR)]
ANIMATION_JUMP_LEFT = [('%s/alien/jlalien.png' % ICON_DIR, ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [('%s/alien/jralien.png' % ICON_DIR, ANIMATION_DELAY)]
ANIMATION_JUMP = [('%s/alien/jalien.png' % ICON_DIR, ANIMATION_DELAY)]
ANIMATION_STAY = [('%s/alien/0alien.png' % ICON_DIR, ANIMATION_DELAY)]
ANIMATION_DIE = [('%s/alien/dalien.png' % ICON_DIR, ANIMATION_DELAY)]
SOUND_JUMP = pygame.mixer.Sound("%s/alien/jump.wav" % ICON_DIR)

#Player sounds
SOUND_DIE = pygame.mixer.Sound("%s/alien/die.wav" % ICON_DIR)
SOUND_STEP = pygame.mixer.Sound("%s/alien/step.wav" % ICON_DIR)
SOUND_COIN = pygame.mixer.Sound("%s/alien/coin.wav" % ICON_DIR)

#Monster settings
MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = "#2110FF"
AMIM_DELAY = 0.25

#Monster animations
ANIMATION_MONSTERHORYSONTAL = [('%s/monsters/fire1.png' % ICON_DIR),
                      ('%s/monsters/fire2.png' % ICON_DIR )]

#Blocks settings
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"