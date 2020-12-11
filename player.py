from pygame import *
import pyganim
from pyganim import *
import os
import blocks
from blocks import *
from monsters import *

pygame.init()
MOVE_SPEED = 3.2
WIDTH = 22
HEIGHT = 32
COLOR =  "#888888"
JUMP_POWER = 8
GRAVITY = 0.35 # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 0.08 # скорость смены кадров

ANIMATION_RIGHT = [('alien/0ralient.png'),
            ('alien/1ralient.png'),
            ('alien/2ralient.png'),
            ('alien/1ralient.png'),
            ('alien/0ralient.png'),
            ('alien/3ralient.png'),
            ('alien/4ralient.png'),]
ANIMATION_LEFT = [('alien/0lalient.png'),
            ('alien/1lalient.png'),
            ('alien/2lalient.png'),
            ('alien/1lalient.png'),
            ('alien/0lalient.png'),
            ('alien/3lalient.png'),
            ('alien/4lalient.png'),]
ANIMATION_JUMP_LEFT = [('alien/jlalien.png', ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [('alien/jralien.png', ANIMATION_DELAY)]
ANIMATION_JUMP = [('alien/jalien.png', ANIMATION_DELAY)]
ANIMATION_STAY = [('alien/0alien.png', ANIMATION_DELAY)]
ANIMATION_DIE = [('alien/dalien.png', ANIMATION_DELAY)]
SOUND_JUMP = pygame.mixer.Sound('alien/jump.wav')
SOUND_DIE = pygame.mixer.Sound('alien/die.wav')
SOUND_STEP = pygame.mixer.Sound('alien/step.wav')
SOUND_COIN = pygame.mixer.Sound('alien/coin.wav')

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0 # скорость вертикального перемещения
        self.onGround = False # На земле ли я?
        self.live = True
        self.win = False
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект

        self.image.fill(Color(COLOR))
        self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным

        #Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.convert_alpha()
        self.boltAnimRight.play()

        #Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.convert_alpha()
        self.boltAnimLeft.play()

        #По-умолчанию, стоим
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.convert_alpha()
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.convert_alpha()
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.convert_alpha()
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.convert_alpha()
        self.boltAnimJump.play()

        self.boltAnimDie = pyganim.PygAnimation(ANIMATION_DIE)
        self.boltAnimDie.convert_alpha()
        self.boltAnimDie.play()
        
        del(boltAnim)


    def update(self, left, right, up, platforms, entities):

        if up:
            if self.onGround: # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                SOUND_JUMP.play()
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))


        if left:
            self.xvel = -MOVE_SPEED # Лево = x - n
            #SOUND_STEP.play()
            self.image.fill(Color(COLOR))
            if up: # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED # Право = x + n
            #SOUND_STEP.play()
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not(left or right): # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel +=  GRAVITY

        self.onGround = False; # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, entities)

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms, entities)

    def die(self):
        self.image.fill(Color(COLOR))
        self.boltAnimDie.blit(self.image, (0, 0))
        SOUND_DIE.play()
        self.live = False

    def win(self):
        return self.win

    def teleporting(self):
        self.rect.x = self.startX
        self.rect.y = self.startY

    def collide(self, xvel, yvel, platforms, entities):

        for platform in platforms:
            if sprite.collide_rect(self, platform): # если есть пересечение платформы с игроком
                
                if isinstance(platform, blocks.BlockDie) or isinstance(platform, Monster): # если пересакаемый блок - blocks.BlockDie
                    self.die()# умираем
                elif isinstance(platform, blocks.End):
                    self.win = True
                elif xvel > 0 and not isinstance(platform, blocks.Half):                      # если движется вправо
                    self.rect.right = platform.rect.left # то не движется вправо

                elif xvel < 0 and not isinstance(platform, blocks.Half):                      # если движется влево
                    self.rect.left = platform.rect.right # то не движется влево

                elif yvel > 0:                      # если падает вниз
                    self.rect.bottom = platform.rect.top # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает

                elif yvel < 0 and not isinstance(platform, blocks.Half):                      # если движется вверх
                    self.rect.top = platform.rect.bottom # то не движется вверх
                    self.yvel = 0.2                 # и энергия прыжка пропадает
                    #Если дать -1 можно получить интересную механику)))
                # elif isinstance(platform, blocks.Coin):
                    # SOUND_COIN.play()
                    # platforms.remove(platform)
                    # entities.remove(platform)
                
                #I delete this
                #if isinstance(platform, blocks.Movable):
                #    if self.rect.y + HEIGHT != platform.getY():
                #        platform.move(self.xvel, platforms)
