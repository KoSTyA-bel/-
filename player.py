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
ICON_DIR = os.path.dirname(__file__)

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
SOUND_DIE = pygame.mixer.Sound("%s/alien/die.wav" % ICON_DIR)
SOUND_STEP = pygame.mixer.Sound("%s/alien/step.wav" % ICON_DIR)
SOUND_COIN = pygame.mixer.Sound("%s/alien/coin.wav" % ICON_DIR)

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.coins = 0
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.yvel = 0 # скорость вертикального перемещения
        self.on_ground = False # На земле ли я?
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
            if self.on_ground: # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                SOUND_JUMP.play()
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))


        if left:
            self.xvel = -MOVE_SPEED # Лево = x - n
            #SOUND_STEP.play()
            self.image.fill(Color(COLOR))
            if up or (abs(self.yvel) > 2 * GRAVITY and  not self.on_ground): # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED # Право = x + n
            #SOUND_STEP.play()
            self.image.fill(Color(COLOR))
            if up or (abs(self.yvel) > 2 * GRAVITY and not self.on_ground):
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not(left or right): # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.on_ground:
            self.yvel +=  GRAVITY

        self.on_ground = False; # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, entities)

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms, entities)

    def die(self):
        self.image.fill(Color(COLOR))
        self.boltAnimDie.blit(self.image, (0, 0))
        SOUND_DIE.play()
        self.live = False
    
    def getCoins(self):
        return self.coins // 3
    
    def isLive(self):
        return self.live
    
    def isWin(self):
        return self.win

    def teleporting(self):
        self.live = True
        self.xvel, self.yvel = 0,0
        self.rect.x = self.startX
        self.rect.y = self.startY

    def collide(self, xvel, yvel, platforms, entities):

        for platform in platforms:
            if sprite.collide_rect(self, platform): # если есть пересечение платформы с игроком
                
                if isinstance(platform, blocks.BlockDie) or isinstance(platform, Monster): # если пересакаемый блок - blocks.BlockDie
                    self.die()# умираем
                    
                elif isinstance(platform, blocks.End):
                    self.win = True
                    
                elif isinstance(platform, blocks.Coin):
                    SOUND_COIN.play()
                    print(self.coins)
                    platforms.remove(platform)
                    entities.remove(platform) 
                    
                elif isinstance(platform, blocks.Magnit):
                    self.rect.top = platform.rect.bottom # то не движется вверх
                    self.yvel -= GRAVITY +0.01 #Нужно для зависания в воздухе
                    
                elif xvel > 0 and not isinstance(platform, blocks.Half):                      # если движется вправо
                    self.rect.right = platform.rect.left # то не движется вправо

                elif xvel < 0 and not isinstance(platform, blocks.Half):                      # если движется влево
                    self.rect.left = platform.rect.right # то не движется влево

                elif yvel > 0:                      # если падает вниз
                    self.rect.bottom = platform.rect.top # то не падает вниз
                    self.on_ground = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает

                elif yvel < 0 and not isinstance(platform, blocks.Half):                      # если движется вверх
                    self.rect.top = platform.rect.bottom # то не движется вверх
                    self.yvel = 0.2                 # и энергия прыжка пропадает
                    #Если дать -1 можно получить интересную механику)))
                
                #I delete this
                #if isinstance(platform, blocks.Movable):
                #    if self.rect.y + HEIGHT != platform.getY():
                #        platform.move(self.xvel, platforms)
