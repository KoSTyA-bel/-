import pygame
from pygame import *
from blocks import *
from monsters import *
from settings import *
#import random

class Level:

    def __init__(self, way):
        self.levelFile = open("%s/{}".format(way) % ICON_DIR, 'r')
        self.playerX = 0
        self.playerY = 0
        self.level = []
        self.platforms = []
        self.entities = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        
        a = int(self.levelFile.readline().replace("\n", ""))
        for i in range(a):
            self.line = self.levelFile.readline()
            self.level.append(self.line[0:len(self.line) - 1])
        
        b = int(self.levelFile.readline().replace("\n",''))
        for i in range(b):
            self.line = self.levelFile.readline().replace("\n",'')
            if self.line == "Player":
                self.playerX = int(self.levelFile.readline().replace("\n",""))
                self.playerY = int(self.levelFile.readline().replace("\n",""))
            if self.line == "Monster":
                mn = Monster(int(self.levelFile.readline().replace("\n","")),
                int(self.levelFile.readline().replace("\n","")),
                int(self.levelFile.readline().replace("\n","")),
                int(self.levelFile.readline().replace("\n","")),
                int(self.levelFile.readline().replace("\n","")),
                int(self.levelFile.readline().replace("\n","")))
                self.entities.add(mn)
                self.platforms.append(mn)
                self.monsters.add(mn) 
                
            #if self.line[0] != "": # если строка не пустая
            #    self.commands = self.line.split() # разбиваем ее на отдельные команды
            #if len(self.commands) > 1: # если количество команд > 1, то ищем эти команды
            #    if self.commands[0] == "player": # если первая команда - player
            #        self.playerX= int(self.commands[1]) # то записываем координаты героя
            #        self.playerY = int(self.commands[2])
            #    if self.commands[0] == "monster": # если первая команда monster, то создаем монстра
            #        mn = Monster(int(self.commands[1]),int(self.commands[2]),int(self.commands[3]),int(self.commands[4]),int(self.commands[5]),int(self.commands[6]))
            #        self.entities.add(mn)
            #        self.platforms.append(mn)
            #        self.monsters.add(mn)
            
            self.convertLvl()
            
    def convertLvl(self):

        x=y=0 # координаты
        for row in self.level: # вся строка
            for col in row: # каждый символ

                if col == "-":
                    pf = Platform(x,y)
                    self.entities.add(pf)
                    self.platforms.append(pf)

                if col == "*":
                    bd = BlockDie(x,y)
                    self.entities.add(bd)
                    self.platforms.append(bd)

                if col == "W":
                    end = End(x,y)
                    self.entities.add(end)
                    self.platforms.append(end)

                if col == "H":
                    m = Half(x,y)
                    self.entities.add(m)
                    self.platforms.append(m)
                    
                if col == "M":
                    m = Magnit(x,y)
                    self.entities.add(m)
                    self.platforms.append(m)
                    
                if col == "C":
                    c = Coin(x,y)
                    self.entities.add(c)
                    self.platforms.append(c)
                    
                # if col == "M":
                    # m = Movable(x,y)
                    # self.entities.add(m)
                    # self.platforms.append(m)
                    
                
                #слишком сильно кушает фпс
                # if col == " ":
                    # r = random.randint(0,2)
                    # if r == 0:
                        # b = Platform(x,y, "block/0.png")
                    # elif r ==1:
                        # b = Platform(x,y, "block/1.png")
                    # else:
                        # b = Platform(x,y, "block/2.png")
                    # self.entities.add(b)

                x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT    #то же самое и с высотой
            x = 0                   #на каждой новой строчке начинаем с нуля

    def getLvl(self):
        return self.level

    def getPlayerX(self):
        return self.playerX

    def getPlayerY(self):
        return self.playerY

    def getEntities(self):
        return self.entities

    def getPlatforms(self):
        return self.platforms
    
    def getMonsters(self):
        return self.monsters
