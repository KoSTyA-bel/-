import sys
import pygame
from pygame import*
from main import *

ICON_DIR = os.path.dirname(__file__)
SOUND_CHOISE = pygame.mixer.Sound("%s/levels/select.wav" % ICON_DIR)
SOUND_ACCEPT = pygame.mixer.Sound("%s/levels/accept.wav" % ICON_DIR)
window = pygame.display.set_mode(DISPLAY)
screen = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))

class Menu:
    def __init__(self, punkts = [400, 350, u'Punkt', (250,250,30), (250,30,250)]):
        self.punkts = punkts
    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]-30))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]-30))
    def showMenu(self):
        done = True
        font_showMenu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0,0)
        pygame.mouse.set_visible(False)
        punkt = 0
        while done:
            screen.fill((0, 100, 200))
            # mp = pygame.mouse.get_pos()
            # for i in self.punkts:
                # if mp[0]>i[0] and mp[0]<i[0]+155 and mp[1]>i[1] and mp[1]<i[1]+50:
                    # punkt =i[5]
            self.render(screen, font_showMenu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                            SOUND_CHOISE.play()
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts)-1:
                            punkt += 1
                            SOUND_CHOISE.play()
                    #отслеживание нажатия Enter
                    if e.key == pygame.K_RETURN:
                        if punkt == 0:
                            SOUND_ACCEPT.play()
                            done = False
                        elif punkt == 1:
                            sys.exit()
                # if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    # if punkt == 0:
                        # done = False
                    # elif punkt == 1:
                        # sys.exit()
            window.blit(screen, (0, 0))
            pygame.display.flip()
