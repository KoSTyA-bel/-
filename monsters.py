from pygame import *
import pyganim
import os
from settings import *

class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, max_length_left,max_length_up):
        self.startX = x # начальные координаты
        self.startY = y
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.max_length_left = max_length_left # максимальное расстояние, которое может пройти в одну сторону
        self.max_length_up = max_length_up # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up # скорость движения по вертикали, 0 - не двигается
        boltAnim = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltAnim.append((anim, AMIM_DELAY))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.convert_alpha()
        self.boltAnim.play()
         
    def update(self, platforms): # по принципу героя
                    
        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
       
        self.rect.y += self.yvel
        self.rect.x += self.xvel
 
        self.collide(platforms)
        
        if (abs(self.startX - self.rect.x) > self.max_length_left):
            self.xvel =-self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
        if (abs(self.startY - self.rect.y) > self.max_length_up):
            self.yvel = -self.yvel # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p: # если с чем-то или кем-то столкнулись
               self.xvel = - self.xvel # то поворачиваем в обратную сторону
               self.yvel = - self.yvel
